#!/usr/bin/env python3
"""Validate and package the distributable Commeto plugin (standard library only)."""
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/commeto"


def build():
    manifest = json.loads((PLUGIN / "plugin.json").read_text())
    assert manifest["name"] == "commeto"
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    assert manifest["author"]["name"] == "biskootmonster"
    listing = manifest["extensions"]["com.openai"]["interface"]
    for key, limit in [("displayName", 30), ("shortDescription", 30),
                       ("developerName", 80), ("longDescription", 4000)]:
        assert 0 < len(listing[key]) <= limit, key
    assert len(listing["defaultPrompt"]) <= 3
    assert all(len(p) <= 128 and "@" not in p for p in listing["defaultPrompt"])
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        assert listing[key].startswith("https://github.com/efter-dash/commeto"), key
    for key in ("composerIcon", "composerIconDark", "logo", "logoDark"):
        assert listing[key].startswith("./") and ".." not in listing[key].split("/")
        asset = PLUGIN / listing[key]
        assert asset.is_file() and asset.stat().st_size <= 5 * 1024 * 1024
        svg = ET.parse(asset).getroot()
        assert int(svg.attrib["width"]) == int(svg.attrib["height"]) >= 48
    skill = PLUGIN / "skills/video-research/SKILL.md"
    assert skill.read_text().startswith("---\nname: video-research\n")
    for link in re.findall(r"\]\(([^)]+)\)", skill.read_text()):
        if "://" not in link:
            assert (skill.parent / link).is_file(), link
    catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    assert (ROOT / catalog["plugins"][0]["source"]["path"]).resolve() == PLUGIN.resolve()
    for path in PLUGIN.rglob("*.json"):
        json.loads(path.read_text())
    shutil.copyfile(ROOT / "LICENSE", PLUGIN / "LICENSE")
    files = sorted(p for p in PLUGIN.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    assert all(not p.is_symlink() for p in files)
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / f"commeto-{manifest['version']}.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            entry = zipfile.ZipInfo(path.relative_to(PLUGIN).as_posix(), (2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert "plugin.json" in archive.namelist()
        assert not any(".." in p.split("/") for p in archive.namelist())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (dist / "SHA256SUMS").write_text(f"{digest}  {target.name}\n")
    print(f"Validated {len(files)} files; built {target.name}; SHA256 {digest}")
    return target


if __name__ == "__main__":
    build()
