"""Shared helpers: token loading and an explicit opt-in before anything is charged."""
import json
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient


def get_client() -> ApifyClient:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN in your environment (see .env.example).")
    return ApifyClient(token)


def run_actor(actor_id: str, run_input: dict, max_charge_usd: float, live: bool) -> list:
    """Print the input; only call the Actor when --run is passed.

    max_charge_usd is passed as the run's maxTotalChargeUsd cap, so a
    pay-per-event Actor stops charging at that amount.
    """
    print(f"Actor: {actor_id}")
    print("Input:", json.dumps(run_input, indent=2))
    if not live:
        print("Dry run (no charge). Re-run with --run to execute.")
        return []
    client = get_client()
    run = client.actor(actor_id).call(
        run_input=run_input,
        max_total_charge_usd=Decimal(str(max_charge_usd)),
    )
    if run is None:
        sys.exit("Run did not return.")
    print("Run status:", run["status"], "| dataset:", run["defaultDatasetId"])
    summary = client.key_value_store(run["defaultKeyValueStoreId"]).get_record("SUMMARY")
    if summary:
        print("SUMMARY:", json.dumps(summary["value"], indent=2))
    return client.dataset(run["defaultDatasetId"]).list_items().items
