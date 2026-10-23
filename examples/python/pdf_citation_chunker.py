"""PDF -> page-aware, citation-ready chunks with skilled_glee/pdf-citation-chunker.

Usage:
    python pdf_citation_chunker.py                       # dry run, prints input
    python pdf_citation_chunker.py --run                 # executes (charged per processed page)
    python pdf_citation_chunker.py --run --url https://example.org/file.pdf
"""
import argparse
import json

from _common import run_actor

ACTOR_ID = "skilled_glee/pdf-citation-chunker"

# Same input as an existing run of this Actor (NIST AI RMF 1.0, public domain).
DEFAULT_URL = "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--chunk-size", type=int, default=3000)
    p.add_argument("--overlap", type=int, default=300)
    p.add_argument("--max-charge-usd", type=float, default=0.05)
    p.add_argument("--run", action="store_true", help="actually call the Actor")
    a = p.parse_args()

    run_input = {"mode": "chunk", "url": a.url, "chunkSize": a.chunk_size, "overlap": a.overlap}
    items = run_actor(ACTOR_ID, run_input, a.max_charge_usd, a.run)
    for item in items[:3]:
        print(json.dumps(
            {k: item[k] for k in ("chunkId", "pageStart", "pageEnd", "estimatedTokens")},
        ))
        print(item["text"][:200].replace("\n", " "), "...")
    if items:
        print(f"{len(items)} chunks")


if __name__ == "__main__":
    main()
