#!/usr/bin/env python3
"""Offline evidence-ledger validation and rubric calculation. Python 3.10+."""
import argparse
import copy
import datetime as dt
import json
import math
import sys
from pathlib import Path
from urllib.parse import urlsplit

TIERS = {
    "integrity": (0.20, ("title_alignment", "presentation_accessibility", "promotional_balance")),
    "authority": (0.30, ("relevant_expertise", "source_transparency", "independent_corroboration")),
    "rigor": (0.30, ("claim_support", "context_and_limits", "currency")),
    "utility": (0.20, ("audience_fit", "explanatory_structure", "learning_support")),
}
DEFAULTS = {"min_credibility_score": 0.75, "require_transcripts": True, "max_results": 5}
RATINGS = (0, 0.25, 0.5, 0.75, 1)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty string required")


def date(value, label):
    text(value, label)
    require(len(value) == 10, f"{label}: use YYYY-MM-DD")
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label}: invalid date") from exc


def url(value, label):
    text(value, label)
    try:
        parts = urlsplit(value)
        require(parts.scheme in ("http", "https") and bool(parts.hostname)
                and not parts.username and not parts.password
                and not any(c.isspace() for c in value), f"{label}: HTTP(S) URL without credentials required")
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{label}: invalid URL") from exc
    return parts


def refs(value, sources, label, required=False):
    require(isinstance(value, list), f"{label}: list required")
    require(all(isinstance(v, str) and v in sources for v in value), f"{label}: unknown source ID")
    require(len(value) == len(set(value)), f"{label}: duplicate source ID")
    require(not required or bool(value), f"{label}: evidence source required")


def validate_candidate(c):
    require(isinstance(c, dict), "candidate must be an object")
    for key in ("id", "title", "creator", "scope"):
        text(c.get(key), key)
    url(c.get("url"), "url")
    require(c.get("transcript") in ("full", "partial", "none"), "invalid transcript status")
    for key in ("content_inspected", "single_core_claim"):
        require(type(c.get(key)) is bool, f"{key}: boolean required")
    require(c.get("filters_status") in ("pass", "unknown", "fail"), "invalid filters_status")
    duration = c.get("duration_seconds")
    require(duration is None or (type(duration) is int and duration > 0),
            "duration_seconds: positive integer or null required")
    if c.get("published_at") is not None:
        date(c["published_at"], "published_at")
    if c.get("language") is not None:
        text(c["language"], "language")
    require(isinstance(c.get("sources"), list), "sources: list required")
    sources = {}
    for s in c["sources"]:
        require(isinstance(s, dict), "source must be an object")
        for key in ("id", "label"):
            text(s.get(key), f"source.{key}")
        require(s["id"] not in sources, "duplicate source ID")
        url(s.get("url"), "source.url")
        date(s.get("accessed_at"), "source.accessed_at")
        require(s.get("kind") in ("video", "transcript", "publisher", "verification", "profile"),
                "invalid source kind")
        sources[s["id"]] = s
    require(isinstance(c.get("tiers"), dict) and set(c["tiers"]) == set(TIERS),
            "tiers: exactly four named tiers required")
    for tier, (_, criteria) in TIERS.items():
        values = c["tiers"][tier]
        require(isinstance(values, dict) and set(values) == set(criteria),
                f"{tier}: all three named criteria required")
        for key, v in values.items():
            require(isinstance(v, dict), f"{key}: object required")
            require("rating" in v, f"{key}: rating required")
            rating = v["rating"]
            require(rating is None or (type(rating) in (int, float)
                    and math.isfinite(rating) and rating in RATINGS),
                    f"{key}: rating must be null, 0, .25, .5, .75, or 1")
            text(v.get("reason"), f"{key}.reason")
            refs(v.get("source_ids"), sources, f"{key}.source_ids", rating is not None)
    require(isinstance(c.get("claims"), list), "claims: list required")
    for claim in c["claims"]:
        require(isinstance(claim, dict), "claim must be an object")
        text(claim.get("text"), "claim.text")
        require(claim.get("status") in ("supported", "contradicted", "unresolved"),
                "invalid claim status")
        settled = claim["status"] != "unresolved"
        refs(claim.get("source_ids"), sources, "claim.source_ids", settled)
        if settled:
            text(claim.get("verification_note"), "claim.verification_note")
            require(any(sources[s]["kind"] == "verification"
                        and sources[s]["url"].split("#")[0] != c["url"].split("#")[0]
                        for s in claim["source_ids"]), "settled claim requires a distinct verification source")
    require(isinstance(c.get("critical_issues"), list), "critical_issues: list required")
    for issue in c["critical_issues"]:
        require(isinstance(issue, dict), "critical issue must be an object")
        text(issue.get("reason"), "critical issue.reason")
        refs(issue.get("source_ids"), sources, "critical issue.source_ids", True)
    require(isinstance(c.get("moments"), list), "moments: list required")
    for moment in c["moments"]:
        require(isinstance(moment, dict), "moment must be an object")
        seconds = moment.get("seconds")
        require(type(seconds) is int and seconds >= 0, "moment.seconds: nonnegative integer required")
        require(duration is None or seconds < duration, "timestamp outside video duration")
        text(moment.get("takeaway"), "moment.takeaway")
        ref = moment.get("source_id")
        require(isinstance(ref, str) and ref in sources, "moment has unknown source ID")
        require(sources[ref]["kind"] in ("video", "transcript", "publisher"),
                "timestamp requires video, transcript, or publisher chapter evidence")
    require(isinstance(c.get("caveats"), list)
            and all(isinstance(x, str) and x.strip() for x in c["caveats"]), "caveats: string list required")


def assess(c, config):
    validate_candidate(c)
    tier_results = {}
    coverage = conservative = 0.0
    missing = []
    quality = []
    hard = []
    for name, (weight, _) in TIERS.items():
        known = [v["rating"] for v in c["tiers"][name].values() if v["rating"] is not None]
        score = sum(known) / len(known) if known else None
        part = len(known) / 3
        tier_results[name] = {"score": round(score, 4) if score is not None else None,
                              "coverage": round(part, 4)}
        coverage += weight * part
        conservative += weight * sum(known) / 3
        if len(known) < 2:
            missing.append(f"{name}: fewer than two assessed criteria")
        if score is not None and score < 0.5:
            quality.append(f"{name}: below the 0.50 tier floor")
    if coverage + 1e-9 < 0.75:
        missing.append("weighted evidence coverage below 0.75")
    if not c["content_inspected"]:
        missing.append("substantive video or transcript content was not inspected")
    if config["require_transcripts"] and c["transcript"] != "full":
        missing.append("full transcript required but unavailable")
    needed = 1 if c["single_core_claim"] else 2
    if len(c["claims"]) < needed:
        missing.append(f"fewer than {needed} core claim checks")
    if any(claim["status"] == "unresolved" for claim in c["claims"]):
        missing.append("unresolved sampled core claims")
    if any(claim["status"] == "contradicted" for claim in c["claims"]):
        hard.append("material core claim contradicted by recorded evidence")
    if c["critical_issues"]:
        hard.append("critical integrity issue supported by recorded evidence")
    if c["filters_status"] == "fail":
        hard.append("does not meet the user's filters")
    elif c["filters_status"] == "unknown":
        missing.append("one or more required filters unverified")
    if conservative + 1e-9 < config["min_credibility_score"]:
        quality.append("below the user's minimum rubric score")
    if hard:
        decision, reasons = "excluded", hard + missing + quality
    elif missing:
        decision, reasons = "provisional", missing + quality
    elif quality:
        decision, reasons = "excluded", quality
    else:
        decision, reasons = "vetted", ["passes recorded evidence and rubric gates within the stated scope"]
    return {**copy.deepcopy(c), "assessment": {
        "decision": decision, "rubric_score": round(conservative, 4) if not missing else None,
        "conservative_score": round(conservative, 4), "coverage": round(coverage, 4),
        "tiers": tier_results, "reasons": reasons}}


def evaluate(payload):
    require(isinstance(payload, dict), "input must be an object")
    text(payload.get("query"), "query")
    supplied = payload.get("config", {})
    require(isinstance(supplied, dict) and set(supplied) <= set(DEFAULTS), "unknown configuration field")
    config = {**DEFAULTS, **supplied}
    score = config["min_credibility_score"]
    require(type(score) in (int, float) and math.isfinite(score) and 0 <= score <= 1,
            "min_credibility_score must be between 0 and 1")
    require(type(config["require_transcripts"]) is bool, "require_transcripts must be boolean")
    require(type(config["max_results"]) is int and 1 <= config["max_results"] <= 20,
            "max_results must be an integer between 1 and 20")
    require(isinstance(payload.get("candidates"), list), "candidates: list required")
    items = [assess(c, config) for c in payload["candidates"]]
    require(len({c["id"] for c in items}) == len(items), "duplicate candidate IDs")
    require(len({c["url"].split("#")[0] for c in items}) == len(items), "duplicate candidate URLs")
    ranked = sorted(items, key=lambda c: (-c["assessment"]["conservative_score"], c["id"]))
    vetted = [c for c in ranked if c["assessment"]["decision"] == "vetted"]
    count = config["max_results"]
    return {
        "schema_version": "1.0.0", "query": payload["query"],
        "assessed_at": dt.datetime.now(dt.timezone.utc).isoformat(), "config": config,
        "results": vetted[:count],
        "provisional": [c for c in ranked if c["assessment"]["decision"] == "provisional"],
        "excluded": [c for c in ranked if c["assessment"]["decision"] == "excluded"],
        "additional_qualified": vetted[count:],
        "summary": {"requested": count, "qualified": len(vetted), "returned": len(vetted[:count]),
                    "shortfall": max(0, count - len(vetted))},
    }


def template():
    return {"query": "Replace with the user's video research question", "config": DEFAULTS.copy(),
            "candidates": [{
                "id": "candidate-1", "url": "https://example.org/video",
                "title": "Replace with verified title", "creator": "Replace with verified creator",
                "duration_seconds": None, "published_at": None, "language": None,
                "scope": "Nothing inspected yet", "transcript": "none", "content_inspected": False,
                "filters_status": "unknown", "sources": [],
                "tiers": {tier: {key: {"rating": None, "reason": "Not examined", "source_ids": []}
                                for key in keys} for tier, (_, keys) in TIERS.items()},
                "claims": [], "single_core_claim": False, "critical_issues": [],
                "moments": [], "caveats": ["Template only; not a real recommendation"]}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="Local evidence ledger JSON")
    parser.add_argument("--output", help="Write report JSON to this file")
    parser.add_argument("--template", action="store_true", help="Print an empty evidence ledger")
    args = parser.parse_args()
    try:
        if args.template:
            result = template()
        else:
            require(bool(args.input), "input JSON path required (or use --template)")
            result = evaluate(json.loads(Path(args.input).read_text(encoding="utf-8")))
        rendered = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        if args.output:
            require(not args.input or Path(args.input).resolve() != Path(args.output).resolve(),
                    "output must not overwrite the evidence input")
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except (ValueError, OSError) as exc:
        print(f"Commeto: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
