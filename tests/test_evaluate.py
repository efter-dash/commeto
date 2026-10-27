import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/commeto/skills/video-research/scripts/evaluate.py"
spec = importlib.util.spec_from_file_location("evaluate", SCRIPT)
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


def fixture():
    data = ev.template()
    data["query"] = "Synthetic fixture for rubric invariants"
    c = data["candidates"][0]
    c.update(transcript="full", content_inspected=True, filters_status="pass", duration_seconds=600)
    c["sources"] = [
        {"id": "transcript", "url": "https://example.org/transcript", "label": "Synthetic transcript",
         "accessed_at": "2026-10-27", "kind": "transcript"},
        {"id": "reference", "url": "https://example.org/reference", "label": "Synthetic reference",
         "accessed_at": "2026-10-27", "kind": "verification"},
    ]
    for tier in c["tiers"].values():
        for criterion in tier.values():
            criterion.update(rating=0.75, reason="Synthetic evidence", source_ids=["reference"])
    c["claims"] = [
        {"text": f"Synthetic claim {i}", "status": "supported", "source_ids": ["reference"],
         "verification_note": "Synthetic primary reference covers this exact claim"}
        for i in range(2)]
    return data


class EvidenceTests(unittest.TestCase):
    def test_threshold_boundary_is_inclusive(self):
        report = ev.evaluate(fixture())
        self.assertEqual(report["results"][0]["assessment"]["rubric_score"], 0.75)
        self.assertEqual(report["summary"]["shortfall"], 4)

    def test_no_evidence_cannot_qualify(self):
        report = ev.evaluate(ev.template())
        self.assertEqual(len(report["results"]), 0)
        self.assertIsNone(report["provisional"][0]["assessment"]["rubric_score"])

    def test_absent_transcript_not_waived(self):
        data = fixture()
        data["candidates"][0]["transcript"] = "none"
        self.assertEqual(len(ev.evaluate(data)["provisional"]), 1)
        self.assertEqual(data["config"]["min_credibility_score"], 0.75)

    def test_explicit_no_transcript_mode_still_requires_content(self):
        data = fixture()
        data["config"]["require_transcripts"] = False
        data["candidates"][0]["transcript"] = "none"
        self.assertEqual(len(ev.evaluate(data)["results"]), 1)
        data["candidates"][0]["content_inspected"] = False
        self.assertEqual(len(ev.evaluate(data)["provisional"]), 1)

    def test_missing_evidence_does_not_inflate_score(self):
        data = fixture()
        c = data["candidates"][0]
        for tier in c["tiers"].values():
            for v in tier.values():
                v["rating"] = 1
            list(tier.values())[0].update(rating=None, source_ids=[], reason="Unknown")
        a = ev.evaluate(data)["provisional"][0]["assessment"]
        self.assertAlmostEqual(a["conservative_score"], 2 / 3, places=4)
        self.assertIsNone(a["rubric_score"])

    def test_contradiction_overrides_missing_evidence(self):
        data = fixture()
        data["candidates"][0]["transcript"] = "none"
        data["candidates"][0]["claims"][0]["status"] = "contradicted"
        self.assertEqual(len(ev.evaluate(data)["excluded"]), 1)

    def test_single_claim_exception_is_explicit(self):
        data = fixture()
        c = data["candidates"][0]
        c["claims"] = c["claims"][:1]
        self.assertEqual(len(ev.evaluate(data)["provisional"]), 1)
        c["single_core_claim"] = True
        self.assertEqual(len(ev.evaluate(data)["results"]), 1)

    def test_unknown_filter_and_failed_filter_differ(self):
        data = fixture()
        data["candidates"][0]["filters_status"] = "unknown"
        self.assertEqual(len(ev.evaluate(data)["provisional"]), 1)
        data["candidates"][0]["filters_status"] = "fail"
        self.assertEqual(len(ev.evaluate(data)["excluded"]), 1)

    def test_unknown_sources_rejected(self):
        data = fixture()
        data["candidates"][0]["claims"][0]["source_ids"] = ["invented"]
        with self.assertRaisesRegex(ValueError, "unknown source"):
            ev.evaluate(data)

    def test_video_cannot_verify_itself(self):
        data = fixture()
        data["candidates"][0]["sources"][1]["url"] = data["candidates"][0]["url"]
        with self.assertRaisesRegex(ValueError, "distinct verification"):
            ev.evaluate(data)

    def test_timestamp_bounds_and_provenance(self):
        data = fixture()
        c = data["candidates"][0]
        c["moments"] = [{"seconds": 10, "takeaway": "Example", "source_id": "transcript"}]
        self.assertEqual(len(ev.evaluate(data)["results"]), 1)
        c["moments"][0]["seconds"] = 600
        with self.assertRaisesRegex(ValueError, "outside video"):
            ev.evaluate(data)
        c["moments"][0].update(seconds=10, source_id="reference")
        with self.assertRaisesRegex(ValueError, "timestamp requires"):
            ev.evaluate(data)

    def test_booleans_not_numbers_and_nonfinite_rejected(self):
        for score in (True, float("nan"), float("inf"), -0.1, 1.1):
            data = fixture()
            data["config"]["min_credibility_score"] = score
            with self.assertRaises(ValueError):
                ev.evaluate(data)

    def test_tier_floor_prevents_averaging_away_failure(self):
        data = fixture()
        for tier in data["candidates"][0]["tiers"].values():
            for v in tier.values():
                v["rating"] = 1
        for v in data["candidates"][0]["tiers"]["integrity"].values():
            v["rating"] = 0.25
        self.assertEqual(len(ev.evaluate(data)["excluded"]), 1)

    def test_limit_and_stable_ranking(self):
        data = fixture()
        second = copy.deepcopy(data["candidates"][0])
        second.update(id="candidate-2", url="https://example.org/second")
        data["candidates"].append(second)
        data["config"]["max_results"] = 1
        report = ev.evaluate(data)
        self.assertEqual(len(report["results"]), 1)
        self.assertEqual(len(report["additional_qualified"]), 1)
        self.assertEqual(report["results"][0]["id"], "candidate-1")

    def test_duplicate_ids_rejected(self):
        data = fixture()
        data["candidates"].append(copy.deepcopy(data["candidates"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate candidate"):
            ev.evaluate(data)

    def test_unresolved_claim_is_provisional(self):
        data = fixture()
        data["candidates"][0]["claims"][0]["status"] = "unresolved"
        self.assertEqual(len(ev.evaluate(data)["provisional"]), 1)

    def test_evaluation_does_not_mutate_evidence(self):
        data = fixture()
        before = copy.deepcopy(data)
        ev.evaluate(data)
        self.assertEqual(data, before)


if __name__ == "__main__":
    unittest.main()
