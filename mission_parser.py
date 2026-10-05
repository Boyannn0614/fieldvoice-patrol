"""Minimal parser for ASR transcripts used in the prototype."""

from __future__ import annotations

import json
import sys


AREA_WORDS = {
    "一號田": "field_1",
    "二號田": "field_2",
    "東區": "east",
    "西區": "west",
    "全部": "all",
}


def parse_mission(transcript: str) -> dict:
    area = next((value for key, value in AREA_WORDS.items() if key in transcript), "unspecified")
    intent = "inspect_water" if any(word in transcript for word in ("積水", "淹水", "巡田", "巡檢")) else "unknown"
    return {
        "transcript": transcript,
        "intent": intent,
        "area": area,
        "requires_human_confirmation": True,
        "ready": intent != "unknown" and area != "unspecified",
    }


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "幫我巡檢一號田有沒有積水"
    print(json.dumps(parse_mission(text), ensure_ascii=False, indent=2))
