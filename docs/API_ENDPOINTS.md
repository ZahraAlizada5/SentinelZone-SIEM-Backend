# API endpoint inventory

Generated from `docs/openapi.json` for v0.28.1. FastAPI utility pages and the hidden root route are not counted.

| Method | Path | Group |
|---|---|---|
| GET | `/v1/incidents/{incident_id}/case-pack` | investigations |
| POST | `/v1/event-sets` | investigations |
| GET | `/v1/replay/rules` | investigations |
| POST | `/v1/replay` | investigations |
| GET | `/v1/replay/{run_id}` | investigations |
| POST | `/v1/assets/{host_id}/snapshots` | investigations |
| GET | `/v1/assets/{host_id}/what-changed` | investigations |
| GET | `/health` | health |
| GET | `/v1/alerts` | alerts |
| GET | `/v1/alerts/{event_uid}` | alerts |
| GET | `/v1/overview` | overview |
| GET | `/v1/assets` | assets |
| PATCH | `/v1/assets/{host_id}` | assets |
| GET | `/v1/agents` | agents |
| GET | `/v1/metrics` | telemetry |
| GET | `/v1/telemetry-health` | telemetry |
| POST | `/v1/telemetry/heartbeat` | telemetry |
| GET | `/v1/incidents` | incidents |
| POST | `/v1/incidents` | incidents |
| GET | `/v1/incidents/{incident_id}` | incidents |
| PATCH | `/v1/incidents/{incident_id}` | incidents |
| GET | `/v1/incidents/{incident_id}/timeline` | incidents |
| POST | `/v1/incidents/{incident_id}/notes` | incidents |
| POST | `/v1/incidents/{incident_id}/merge` | incidents |
| GET | `/v1/merge-requests` | merge-requests |
| POST | `/v1/merge-requests/{mid}/approve` | merge-requests |
| POST | `/v1/merge-requests/{mid}/reject` | merge-requests |
| GET | `/v1/notifications` | notifications |
| POST | `/v1/notifications/dispatch` | notifications |
| POST | `/v1/hunts/{approved_query_id}/run` | hunts |
| POST | `/v1/admin/ingest/run` | admin |
| GET | `/v1/admin/users` | admin |
| POST | `/v1/admin/users` | admin |
| PATCH | `/v1/admin/users/{username}` | admin |
| POST | `/v1/admin/users/{username}/rotate-token` | admin |
| GET | `/v1/admin/roles` | admin |
| GET | `/v1/action-proposals` | action-proposals |
| POST | `/v1/action-proposals` | action-proposals |
| POST | `/v1/action-proposals/{proposal_id}/approve` | action-proposals |
| POST | `/v1/action-proposals/{proposal_id}/reject` | action-proposals |
