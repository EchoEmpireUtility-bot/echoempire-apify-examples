// Shared helper: prints input, and only calls the Actor when --run is passed.
import { ApifyClient } from 'apify-client';

export const LIVE = process.argv.includes('--run');

export async function runActor(actorId, input, maxTotalChargeUsd) {
    console.log(`Actor: ${actorId}`);
    console.log('Input:', JSON.stringify(input, null, 2));
    if (!LIVE) {
        console.log('Dry run (no charge). Re-run with --run to execute.');
        return [];
    }
    if (!process.env.APIFY_TOKEN) throw new Error('Set APIFY_TOKEN (see .env.example).');
    const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
    // maxTotalChargeUsd caps what a pay-per-event Actor can charge for this run.
    const run = await client.actor(actorId).call(input, { maxTotalChargeUsd });
    console.log(`Run status: ${run.status} | dataset: ${run.defaultDatasetId}`);
    const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
    if (summary) console.log('SUMMARY:', JSON.stringify(summary.value, null, 2));
    const { items } = await client.dataset(run.defaultDatasetId).listItems();
    return items;
}
