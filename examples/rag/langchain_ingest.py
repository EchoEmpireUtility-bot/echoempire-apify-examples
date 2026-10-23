"""Ingest PDF Citation Chunker output into a LangChain vector store, with citations.

Each Actor record already is a chunk, so no text splitter is needed. The
record's chunkId (SHA-256 based, stable for the same PDF + settings) is used
as the vector-store ID, so re-ingesting the same document upserts, not duplicates.

Usage:
    # offline, using the sample records shipped in ../../sample-output (no Apify call, no charge)
    python langchain_ingest.py --from-file ../../sample-output/pdf-citation-chunker.nist-ai-rmf.first5.jsonl

    # live: run the Actor (charged per processed page) and ingest its dataset
    python langchain_ingest.py --url https://example.org/doc.pdf --run

Swap DeterministicFakeEmbedding for a real embedding model (OpenAIEmbeddings,
HuggingFaceEmbeddings, ...) and InMemoryVectorStore for your production store.
"""
import argparse
import json
import os
import sys
from decimal import Decimal

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.vectorstores import InMemoryVectorStore

ACTOR_ID = "skilled_glee/pdf-citation-chunker"
METADATA_KEYS = (
    "sourceUrl", "documentId", "documentTitle", "pageStart", "pageEnd",
    "chunkIndex", "chunkId", "sha256", "estimatedTokens",
)


def load_from_file(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        if path.endswith(".jsonl"):
            return [json.loads(line) for line in fh if line.strip()]
        data = json.load(fh)
        return data if isinstance(data, list) else [data]


def load_from_actor(url: str, max_charge_usd: float) -> list:
    from apify_client import ApifyClient

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN.")
    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(
        run_input={"mode": "chunk", "url": url, "chunkSize": 3000, "overlap": 300},
        max_total_charge_usd=Decimal(str(max_charge_usd)),
    )
    if run is None:
        sys.exit("Run did not return.")
    return client.dataset(run["defaultDatasetId"]).list_items().items


def to_documents(records: list) -> list:
    return [
        Document(page_content=r["text"], metadata={k: r.get(k) for k in METADATA_KEYS})
        for r in records
    ]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--from-file")
    p.add_argument("--url")
    p.add_argument("--max-charge-usd", type=float, default=0.05)
    p.add_argument("--run", action="store_true")
    p.add_argument("--query", default="What does the framework say about trustworthy AI?")
    a = p.parse_args()

    if a.from_file:
        records = load_from_file(a.from_file)
    elif a.url and a.run:
        records = load_from_actor(a.url, a.max_charge_usd)
    else:
        sys.exit("Use --from-file PATH, or --url URL --run to call the Actor.")

    docs = to_documents(records)
    store = InMemoryVectorStore(embedding=DeterministicFakeEmbedding(size=256))
    store.add_documents(docs, ids=[d.metadata["chunkId"] for d in docs])
    print(f"Ingested {len(docs)} chunks")

    for hit in store.similarity_search(a.query, k=3):
        m = hit.metadata
        print(f"[{m['documentTitle']}, p.{m['pageStart']}] {m['sourceUrl']}  {m['chunkId'][:23]}...")
        print("   ", hit.page_content[:160].replace("\n", " "))


if __name__ == "__main__":
    main()
