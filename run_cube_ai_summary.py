#!/usr/bin/env python3

import json
import pathlib
from services.cube_protocol import CubeProtocol

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / "cube" / "ai-summary-template.json"
OUTPUT_JSON = ROOT / "cube" / "ai-summary.json"
OUTPUT_CUBE = ROOT / "cube" / "ai-summary.cube"


def main():
    print("🚀 Generating AI Summary Cube…")

    # Load template
    with TEMPLATE.open("r", encoding="utf-8") as f:
        template = json.load(f)

    # Convert original payload to compact JSON
    payload_text = json.dumps(template["original_payload"], separators=(",", ":"))

    # Compress using CUBE Protocol
    cube = CubeProtocol.compress(
        data=payload_text,
        domain="AI_SUMMARY",
        sequence="WEB[PHILHILLS.COM,PHILHILLS.AI]→AICUBE[TEXT]",
        outcome="STORED"
    )

    obj = cube.as_dict()

    # Write human-readable JSON output
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

    # Write raw cube data (flattened cube)
    with OUTPUT_CUBE.open("wb") as f:
        f.write(cube.data.encode("ascii"))

    print("✨ Done: ai-summary.json + ai-summary.cube generated.")


if __name__ == "__main__":
    main()
