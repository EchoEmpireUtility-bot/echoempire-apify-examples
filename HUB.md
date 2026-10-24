# EchoEmpire Actors on Apify — content hub

Deterministic, machine-readable tools for AI agents, RAG pipelines and MCP clients, published on Apify Store by `skilled_glee`. Every Actor below is pay-per-event: you are charged per useful result as listed on its Pricing tab (the live Pricing tab is authoritative).

Connect any of them to an MCP client through Apify's MCP server (`https://mcp.apify.com`), call them from code with `apify-client`, or run them in Apify Console.

> Examples repo: https://github.com/EchoEmpireUtility-bot/echoempire-apify-examples

## Document → RAG chunks (citation-ready)

| Actor | What it does | Price (FREE tier, per live listing) |
|---|---|---|
| [PDF Citation Chunker](https://apify.com/skilled_glee/pdf-citation-chunker) | Turn public embedded-text PDFs into page-aware PDF RAG chunks with citation-ready JSON, source URLs, and SHA-256 provenance IDs. Built for retrieval pipelines and AI agents. No OCR or private PDFs. | `page-processed` $0.00025 |
| [OCR Citation Chunker](https://apify.com/skilled_glee/ocr-citation-chunker) | Extract text from scanned or image-only PDFs into page-aware JSON chunks for RAG and vector database ingestion, with OCR confidence, page citations, provenance, and stable chunk IDs. | `apify-actor-start` $0.00005; `page-processed` $0.0015 |
| [10-K Risk Factors & MD&A Extractor for AI Agents & RAG](https://apify.com/skilled_glee/sec-filing-section-chunker) | For AI agents and RAG pipelines: extract 10-K Item 1A Risk Factors, Item 7 MD&A, Item 7A Market Risk and Item 1 Business sections from plain-text SEC 10-K filings into citation-ready JSON chunks with offsets and SHA-256 hashes. Input: raw text or a public plain-text URL. | `document-converted` $0.005 |
| [SRT & WebVTT to JSON Subtitle Chunker for RAG](https://apify.com/skilled_glee/subtitle-rag-chunker) | Parse SRT and WebVTT subtitle files (raw text or a public URL) into timestamped JSON chunks for AI agents, video transcript RAG and vector databases. Whole cues are never split; chunks keep start/end times in ms, cue numbers where present, stable chunk IDs and SHA-256 hashes. | `document-converted` $0.005 |
| [Legal Opinion Citation Extractor](https://apify.com/skilled_glee/legal-opinion-citation-extractor) | Extract supported full case citations from plain-text court opinions with paragraph and available page provenance. | `document-converted` $0.005 |

## Web and content extraction

| Actor | What it does | Price (FREE tier, per live listing) |
|---|---|---|
| [Website Content Extractor](https://apify.com/skilled_glee/website-content-extractor) | Web page URLs in, clean readable content out. Strips navigation, ads, and boilerplate. Returns title, description, clean text, word count, language. Deterministic, no AI, no browser. | `page-extracted` $0.002646 |
| [Smart Article Extractor](https://apify.com/skilled_glee/article-text-extractor) | Article URLs in, structured article data out. Title, author, published date, clean text, word count, content hash. Handles JSON-LD, bylines, missing dates. Deterministic, no AI, no browser. | `article-extracted` $0.001 |
| [Web Metadata Extractor — Open Graph, JSON-LD as JSON](https://apify.com/skilled_glee/web-metadata-extractor) | Extract machine-useful metadata from web pages as JSON: title, description, Open Graph, Twitter Card, JSON-LD structured data, canonical URL, language, headings. Plain HTTP fetch, no AI, no browser. One failed page never kills the batch. | `page-processed` $0.001 |
| [Contact Details Extractor](https://apify.com/skilled_glee/contact-details-extractor) | Extract contact details from web pages as structured JSON. Give it page URLs, get back emails, phone numbers, social profile links, and contact-page links per page. Deterministic: plain HTTP fetch with pattern extraction, no AI, no browser. One failed page never kills the batch. | `page-processed` $0.0015 |
| [Search Evidence Validator](https://apify.com/skilled_glee/search-evidence-validator) | Validate public search-result URLs for relevance, freshness, content depth, citation readiness, reachability, and deterministic evidence quality before downstream agent use. | `validated-page` $0.01005; `apify-actor-start` $0.00005 |

## Video and social data

| Actor | What it does | Price (FREE tier, per live listing) |
|---|---|---|
| [YouTube Transcript Extractor](https://apify.com/skilled_glee/youtube-transcript-extractor) | YouTube video URLs in, timestamped transcript JSON out. Reads YouTube's published caption tracks directly: no AI, no browser. Per-video segments with start times and text. One failed video never kills the batch. | `transcript-extracted` $0.0084 |
| [YouTube Comments Extractor](https://apify.com/skilled_glee/youtube-comments-extractor) | Extract YouTube video comments as structured JSON: author, text, like count, timestamp, reply count. Give it video URLs, get back per-comment records. Deterministic extraction, no AI, no browser. One failed video never kills the batch. | `comment-extracted` $0.0015 |
| [YouTube Channel Videos](https://apify.com/skilled_glee/youtube-channel-videos) | List a YouTube channel's videos as structured JSON: video ID, title, URL, duration, view count, upload date. Give it channel URLs or handles, get back per-video records. Deterministic extraction, no AI, no browser. | `video-listed` $0.00098 |

## Jobs data

| Actor | What it does | Price (FREE tier, per live listing) |
|---|---|---|
| [LinkedIn Jobs](https://apify.com/skilled_glee/linkedin-jobs) | Search LinkedIn jobs and get structured listings as JSON: title, company, location, posting date, direct URL. Give it keyword queries with an optional location. Uses LinkedIn's public job API, no login, no AI, no browser. | `job-extracted` $0.0015 |
| [Remote Jobs](https://apify.com/skilled_glee/remote-jobs) | Remote job listings search API. Returns job titles, companies, locations, and descriptions. NOTE: relevance scoring is currently degraded. Deterministic search, no AI. | `job-extracted` $0.0045 |

## Agent reliability and Actor tooling

| Actor | What it does | Price (FREE tier, per live listing) |
|---|---|---|
| [Retry Oracle — Deterministic Retry and Spend Decisions](https://apify.com/skilled_glee/retry-oracle) | Failed operation plus attempt, deadline, spend and idempotency context → RETRY, MUTATE or ABORT with reason codes, bounded delays and SHA-256 provenance. No LLM and no operation execution. | `decision-produced` $0.002 |
| [Actor Quality Guard](https://apify.com/skilled_glee/actor-quality-guard) | Audit Apify Actors for contract integrity, machine discovery, execution readiness, pricing, safety, and Store readiness. Returns deterministic scores, blockers, rule IDs, and repair recommendations. | `apify-actor-start` $0.00005; `apify-default-dataset-item` $0.00001; `quality-report-produced` $0.001 |
| [Portfolio Activation Bridge](https://apify.com/skilled_glee/EchoEmpire-Machine-Foundry) | Audit up to 25 Apify Actors for machine discovery and revenue readiness. Get activation scores, blockers, capability cards, public-task drafts, schemas, and REST, Python, and MCP integration metadata. | `actor-audited` $0.001 |
| [Capability Contract Repair Bridge](https://apify.com/skilled_glee/EchoEmpire-Machine-Foundry-1) | Repair incomplete Apify Actor capability contracts into validated schemas, JSON Patch operations, capability cards, public-task drafts, blockers, and REST, Python, and MCP metadata. | `repair-bundle-produced` $0.001 |

## Notes

- Each listing documents its own processing method; most describe deterministic extraction with no AI and no browser. Check the README of the Actor you use.
- Remote Jobs currently states on its own listing that relevance scoring is degraded.
- Prices were read from the live Apify listings on 2026-10-23 and can change; check each Actor's Pricing tab before running.
- Maintainer: EchoEmpire.
