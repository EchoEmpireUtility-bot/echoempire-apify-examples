# Citation-ready RAG chunks from PDFs, 10-K filings and subtitles (Apify Actors)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Code examples for three pay-per-event [Apify](https://apify.com) Actors that turn documents into **deterministic, citation-ready JSON chunks** for RAG pipelines, AI agents and MCP clients:

| Actor | Input | Each output chunk carries | Price as listed (FREE tier) |
|---|---|---|---|
| [PDF Citation Chunker](https://apify.com/skilled_glee/pdf-citation-chunker) | Public embedded-text PDF URL(s), up to 25 per run | page number(s), document title, `chunkId`, SHA-256, `estimatedTokens` | $0.00025 per page that yields chunks |
| [10-K Risk Factors & MD&A Extractor](https://apify.com/skilled_glee/sec-filing-section-chunker) | Plain-text 10-K (raw text or public text URL), up to 25 per run | `sectionItem` (1, 1A, 7, 7A), heading, character offsets, `chunkId`, SHA-256 | $0.005 per document with useful output |
| [SRT & WebVTT to JSON Subtitle Chunker for RAG](https://apify.com/skilled_glee/subtitle-rag-chunker) | SRT or WebVTT (raw text or public URL) | `startTimestampMs`/`endTimestampMs`, cue numbers, `chunkId`, SHA-256. Cues are never split | $0.005 per document with useful output, platform costs included |

Prices come from the live listings on 2026-10-23. The Pricing tab on each listing is authoritative.

See [HUB.md](HUB.md) for every EchoEmpire Actor.

## Why use these for RAG

- **Citations come built in.** Every chunk records where it came from: PDF page, 10-K Item and offsets, or subtitle timestamps. Your agent can cite "p. 9" or "00:01:12" without extra bookkeeping.
- **Stable IDs.** `chunkId` is SHA-256 based and the READMEs say it is stable for identical input and chunking settings. Use it as your vector-store primary key so re-ingesting a document upserts instead of duplicating.
- **Partial failure isolation.** One bad document in a batch gets a failed outcome in the run's `SUMMARY` record. It doesn't wipe out the other documents' output.
- **Charged only for useful output.** Per the listings, empty or failed documents/pages are not charged.
- **Deterministic.** No LLM rewriting inside the Actors, and the source text is not summarised.

## Quick start

```bash
git clone https://github.com/EchoEmpireUtility-bot/echoempire-apify-examples.git
cd echoempire-apify-examples
cp .env.example .env    # add your Apify API token (Console → Settings → API & Integrations)
export $(cat .env | xargs)
```

Every script is a **dry run by default**: it prints the input it would send and exits without charging. Add `--run` to execute. Each run passes a `maxTotalChargeUsd` cap.

### Python

```bash
cd examples/python
pip install -r requirements.txt
python pdf_citation_chunker.py            # dry run
python pdf_citation_chunker.py --run      # NIST AI RMF 1.0 PDF, capped at $0.05
python sec_10k_sections.py --file my_10k.txt --items 1A 7 --run
python subtitle_rag_chunks.py --file talk.vtt --run
```

### JavaScript (Node 18+)

```bash
cd examples/js
npm install
node pdf-citation-chunker.mjs --run
node sec-10k-sections.mjs my_10k.txt --run
node subtitle-rag-chunks.mjs talk.vtt --run
```

### RAG ingestion (LangChain)

`examples/rag/langchain_ingest.py` turns Actor records into LangChain `Document`s, keeps page and source metadata for citations, and uses `chunkId` as the vector ID.

```bash
cd examples/rag
pip install -r requirements.txt
# Offline, no Apify call: uses real records saved from a past run
python langchain_ingest.py --from-file ../../sample-output/pdf-citation-chunker.nist-ai-rmf.first5.jsonl
# Live
python langchain_ingest.py --url https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf --run
```

Swap `DeterministicFakeEmbedding` and `InMemoryVectorStore` for your real embedding model and vector DB.

### MCP (Claude Desktop, Cursor, VS Code, any MCP client)

See [`mcp/`](mcp/README.md). Discovery-only (no token, can't run anything):

```json
{ "mcpServers": { "apify-discovery": { "url": "https://mcp.apify.com?tools=search-actors,fetch-actor-details" } } }
```

The three chunkers as callable tools (OAuth on first connect):

```json
{ "mcpServers": { "apify-chunkers": { "url": "https://mcp.apify.com?tools=skilled_glee/pdf-citation-chunker,skilled_glee/sec-filing-section-chunker,skilled_glee/subtitle-rag-chunker" } } }
```

## Real output

`sample-output/` holds records copied unmodified from an earlier run of PDF Citation Chunker on the public-domain [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) PDF (`chunkSize` 3000, `overlap` 300). That run produced 55 chunks from 48 pages. One record:

```json
{
  "sourceUrl": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
  "documentTitle": "Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
  "pageStart": 9,
  "pageEnd": 9,
  "chunkIndex": 11,
  "pageChunkIndex": 1,
  "chunkId": "sha256:eb84854da2821a56236aad788a57454e95d55b20602321416e0bd988da143876",
  "chunking": { "chunkSize": 3000, "overlap": 300 },
  "text": "NIST AI 100-1 AI RMF 1.0\nPart 1: Foundational Information\n1. Framing Risk\nAI risk management offers a path to minimize potential negative impacts of AI systems, ...",
  "characterCount": 2750,
  "estimatedTokens": 688,
  "extractionMethod": "pypdf"
}
```

(Text truncated here. The full record is in `sample-output/pdf-citation-chunker.nist-ai-rmf.chunk11.json`.)

SEC and subtitle sample output: not included yet. The output fields are documented below.

## Output fields

**PDF:** `sourceUrl, resolvedUrl, sourceByteSize, documentSha256, documentId, documentIndex, documentTitle, pageStart, pageEnd, chunkIndex, pageChunkIndex, chunkId, chunking, text, characterCount, estimatedTokens, sha256, extractionMethod, processedAt`

**10-K:** `sourceUrl, sourceName, documentIndex, documentSha256, documentId, sectionItem, sectionHeading, sectionStartOffset, sectionEndOffset, chunkIndex, sectionChunkIndex, chunkStartOffset, text, characterCount, sha256, chunkId, chunking`

**Subtitles:** `sourceUrl, sourceName, documentIndex, documentSha256, documentId, format, chunkIndex, cueNumbers, startTimestampMs, endTimestampMs, cueCount, text, characterCount, sha256, chunkId, chunking`

Each run also writes a `SUMMARY` record to the default key-value store with per-document outcomes.

## Limits (from the Actor READMEs)

- **PDF:** embedded-text PDFs only (no OCR; for scans use [OCR Citation Chunker](https://apify.com/skilled_glee/ocr-citation-chunker)), public URLs only, 50 MB per PDF, 25 PDFs per run.
- **10-K:** plain text only (convert HTML first). It does not fetch from EDGAR, parse XBRL or verify filing type, and it covers Items 1, 1A, 7 and 7A only. 2 MB per document, 120 s run timeout.
- **Subtitles:** SRT and WebVTT only (no TTML, ASS/SSA, OCR, translation or speaker diarization). 2 MB per document, 120 s run timeout.

## Troubleshooting

- `no_extractable_text` in the PDF `SUMMARY`: the PDF is scanned. Use OCR Citation Chunker.
- A 10-K returns no sections: make sure the input is plain text with `Item 1A.`-style headings, not HTML.
- `spending_limit_reached`: raise `--max-charge-usd`. Unprocessed URLs are listed in `SUMMARY.unprocessedUrls`.

## More Actors

All EchoEmpire Actors: [HUB.md](HUB.md) · Apify Store profile: https://apify.com/skilled_glee

## Contributing

Issues and PRs for new integration examples are welcome.

## License

MIT. See [LICENSE](LICENSE). The Actors themselves are paid services on Apify, governed by Apify's terms.
