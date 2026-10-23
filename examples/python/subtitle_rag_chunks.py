"""SRT / WebVTT -> timestamped, cue-preserving chunks with skilled_glee/subtitle-rag-chunker.

Usage:
    python subtitle_rag_chunks.py                    # dry run with the listing's fixture
    python subtitle_rag_chunks.py --file talk.vtt --run
"""
import argparse
import json

from _common import run_actor

ACTOR_ID = "skilled_glee/subtitle-rag-chunker"

# Fixture text taken verbatim from the Actor's own input prefill.
FIXTURE = (
    "1\n00:00:00,000 --> 00:00:02,000\nDeterministic subtitle health fixture.\n\n"
    "2\n00:00:02,000 --> 00:00:04,000\nThe same input produces the same stable chunk identifiers."
)


def ms_to_ts(ms: int) -> str:
    s, ms = divmod(ms, 1000)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="path to an .srt or .vtt file")
    p.add_argument("--source-name", default="apify-health-fixture")
    p.add_argument("--chunk-size", type=int, default=1500)
    p.add_argument("--overlap", type=int, default=150)
    p.add_argument("--max-charge-usd", type=float, default=0.01)
    p.add_argument("--run", action="store_true")
    a = p.parse_args()

    raw_text = FIXTURE
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            raw_text = fh.read()

    run_input = {"items": [{
        "rawText": raw_text,
        "sourceName": a.source_name,
        "chunkSize": a.chunk_size,
        "overlap": a.overlap,
    }]}
    for item in run_actor(ACTOR_ID, run_input, a.max_charge_usd, a.run):
        span = f"{ms_to_ts(item['startTimestampMs'])}-{ms_to_ts(item['endTimestampMs'])}"
        print(json.dumps({"span": span, "cues": item["cueNumbers"], "chunkId": item["chunkId"]}))
        print(item["text"][:200])


if __name__ == "__main__":
    main()
