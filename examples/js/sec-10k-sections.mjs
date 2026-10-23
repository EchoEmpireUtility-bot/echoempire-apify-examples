// Plain-text 10-K -> Item 1 / 1A / 7 / 7A chunks (skilled_glee/sec-filing-section-chunker).
// node sec-10k-sections.mjs [path/to/10k.txt] [--run]
import { readFileSync } from 'node:fs';
import { runActor } from './common.mjs';

// Fixture text taken verbatim from the Actor's own input prefill.
const FIXTURE = 'Item 1. Business\nEcho Fixture Corp builds deterministic software utilities for machine workflows.\n\n'
    + 'Item 1A. Risk Factors\nService availability and input quality may affect processing results.\n\n'
    + 'Item 7. Management Discussion\nOperations remained intentionally small and deterministic during the fixture period.\n\n'
    + 'Item 7A. Market Risk\nThe fixture has no material market-risk exposure.';

const file = process.argv.slice(2).find((a) => !a.startsWith('--'));
const rawText = file ? readFileSync(file, 'utf8') : FIXTURE;

const input = {
    items: [{
        rawText,
        sourceName: file ?? 'apify-health-fixture',
        requestedItems: ['1', '1A', '7', '7A'],
        chunkSize: 1500,
        overlap: 150,
    }],
};

const items = await runActor('skilled_glee/sec-filing-section-chunker', input, 0.01);
for (const it of items) {
    console.log({ item: it.sectionItem, heading: it.sectionHeading, chunkId: it.chunkId });
}
