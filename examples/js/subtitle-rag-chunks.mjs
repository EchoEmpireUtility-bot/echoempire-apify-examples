// SRT / WebVTT -> timestamped, cue-preserving chunks (skilled_glee/subtitle-rag-chunker).
// node subtitle-rag-chunks.mjs [path/to/file.vtt] [--run]
import { readFileSync } from 'node:fs';
import { runActor } from './common.mjs';

// Fixture text taken verbatim from the Actor's own input prefill.
const FIXTURE = '1\n00:00:00,000 --> 00:00:02,000\nDeterministic subtitle health fixture.\n\n'
    + '2\n00:00:02,000 --> 00:00:04,000\nThe same input produces the same stable chunk identifiers.';

const file = process.argv.slice(2).find((a) => !a.startsWith('--'));
const input = {
    items: [{
        rawText: file ? readFileSync(file, 'utf8') : FIXTURE,
        sourceName: file ?? 'apify-health-fixture',
        chunkSize: 1500,
        overlap: 150,
    }],
};

const items = await runActor('skilled_glee/subtitle-rag-chunker', input, 0.01);
for (const it of items) {
    console.log({ startMs: it.startTimestampMs, endMs: it.endTimestampMs, cues: it.cueNumbers, chunkId: it.chunkId });
    console.log(it.text.slice(0, 200));
}
