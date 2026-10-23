"""Plain-text 10-K -> Item 1 / 1A / 7 / 7A chunks with skilled_glee/sec-filing-section-chunker.

The Actor takes PLAIN TEXT (convert HTML filings to text first). It does not
fetch from EDGAR, parse XBRL, or verify filing type.

Usage:
    python sec_10k_sections.py                      # dry run with the listing's fixture text
    python sec_10k_sections.py --file my_10k.txt    # dry run with your own text
    python sec_10k_sections.py --file my_10k.txt --items 1A 7 --run
"""
import argparse
import json

from _common import run_actor

ACTOR_ID = "skilled_glee/sec-filing-section-chunker"

# Fixture text taken verbatim from the Actor's own input prefill.
FIXTURE = (
    "Item 1. Business\nEcho Fixture Corp builds deterministic software utilities for machine workflows.\n\n"
    "Item 1A. Risk Factors\nService availability and input quality may affect processing results.\n\n"
    "Item 7. Management Discussion\nOperations remained intentionally small and deterministic during the fixture period.\n\n"
    "Item 7A. Market Risk\nThe fixture has no material market-risk exposure."
)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="path to a plain-text 10-K")
    p.add_argument("--source-name", default="apify-health-fixture")
    p.add_argument("--items", nargs="+", default=["1", "1A", "7", "7A"], choices=["1", "1A", "7", "7A"])
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
        "requestedItems": a.items,
        "chunkSize": a.chunk_size,
        "overlap": a.overlap,
    }]}
    for item in run_actor(ACTOR_ID, run_input, a.max_charge_usd, a.run):
        print(json.dumps({k: item[k] for k in ("sectionItem", "sectionHeading", "chunkId", "characterCount")}))


if __name__ == "__main__":
    main()
