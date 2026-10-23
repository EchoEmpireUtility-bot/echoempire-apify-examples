# MCP configs (Apify MCP server)

These follow Apify's official MCP docs: https://docs.apify.com/integrations/mcp

| File | What it gives your agent | Auth |
|---|---|---|
| `apify-mcp.discovery-only.json` | `search-actors` and `fetch-actor-details` only. The agent can find these Actors and read their input schema, README and pricing. It cannot run anything. | None needed |
| `apify-mcp.chunkers.json` | The three chunker Actors as callable tools (hosted server). | OAuth sign-in on first connect, or add `"headers": {"Authorization": "Bearer <APIFY_TOKEN>"}` |
| `apify-mcp.chunkers.stdio.json` | The same tools, run locally with `npx @apify/actors-mcp-server`. | `APIFY_TOKEN` env var |

Running an Actor through MCP is a paid, pay-per-event action. Set a run cap (`maxTotalChargeUsd` in the call options) in your agent's tool policy. Keep tokens in the client's secret store, never in a prompt.

The Apify MCP server excludes full-permission Actors. All three chunkers are published with limited permissions (`actorPermissionLevel: LIMITED_PERMISSIONS` on 2026-10-23).
