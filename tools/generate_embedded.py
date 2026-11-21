"""Regenerate the embedded TPK2 sprite arrays from the preserved assets."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true", help="Check without writing")
args = parser.parse_args()
metadata = json.loads((ROOT / "evidence/embedded-assets.json").read_text())
parts = ["// Generated from the official TamaPoke sprites.pak. PMD SpriteCollab, CC BY-NC.\n#include \"embedded_mon.h\"\nnamespace {\n"]
for asset in metadata:
    data = (ROOT / "assets" / asset["file"]).read_bytes()
    if len(data) != asset["size_bytes"] or hashlib.sha256(data).hexdigest() != asset["sha256"]:
        raise SystemExit("Asset checksum mismatch: " + asset["file"])
    if data[:4] != b"TPK2":
        raise SystemExit("Invalid sprite: " + asset["file"])
    symbol = Path(asset["file"]).stem
    parts.append("const uint8_t " + symbol + "[] = {\n")
    for pos in range(0, len(data), 24):
        parts.append(",".join("0x" + data[i:i + 1].hex() for i in range(pos, min(pos + 24, len(data)))) + ",\n")
    parts.append("};\n")
parts.append("}\nconst uint8_t *embeddedMonData(uint8_t dex, bool shiny, uint32_t &size) {\n")
parts.append("  switch (dex) {\n")
for dex in [25, 26]:
    normal, shiny = f"p{dex:03d}", f"ps{dex:03d}"
    parts.append(f"    case {dex}: size = shiny ? sizeof({shiny}) : sizeof({normal}); return shiny ? {shiny} : {normal};\n")
parts.append("    default: size = 0; return nullptr;\n  }\n}\n")
generated = "".join(parts)
destination = ROOT / "TamaPoke/embedded_mon.cpp"
if args.check:
    if destination.read_text() != generated:
        raise SystemExit("Embedded source differs; run python3 tools/generate_embedded.py")
    print("Embedded asset checksums and generated source match")
else:
    destination.write_text(generated)
    print("Generated", destination)
