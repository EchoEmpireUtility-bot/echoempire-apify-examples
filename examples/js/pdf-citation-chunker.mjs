// PDF -> page-aware, citation-ready chunks (skilled_glee/pdf-citation-chunker).
// node pdf-citation-chunker.mjs [--run]
import { runActor } from './common.mjs';

// Same input as an existing run of this Actor (NIST AI RMF 1.0, public domain).
const input = {
    mode: 'chunk',
    url: 'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf',
    chunkSize: 3000,
    overlap: 300,
};

const items = await runActor('skilled_glee/pdf-citation-chunker', input, 0.05);
for (const it of items.slice(0, 3)) {
    console.log({ chunkId: it.chunkId, page: it.pageStart, tokens: it.estimatedTokens });
    console.log(`${it.text.slice(0, 200).replace(/\n/g, ' ')} ...`);
}
if (items.length) console.log(`${items.length} chunks`);
