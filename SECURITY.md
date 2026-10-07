# Security policy

## Supported development release

This handoff targets **0.28.1**, a development/integration release. It does not establish a long-term support period or certify production readiness. Current local checks and open gates are documented in [STATUS.md](docs/STATUS.md).

## Reporting a vulnerability

Do not publish exploitable details, credentials, private keys, database dumps, captured honeypot passwords, or real customer/lab events in a public issue or PR.

Use this GitHub repository's **Security → Report a vulnerability** private reporting option if the owner has enabled it. Its availability has not been verified. If unavailable, use an existing verified private contact with the repository owner, or open a minimal public request asking for a private reporting channel without disclosing the vulnerability. No unverified email address is supplied here.

Include the affected release, sanitized reproduction, impact, and environment assumptions. Coordinate disclosure and a fix with the owner before publication. No response-time or bounty commitment is promised without owner approval. The owner should enable a private reporting channel before public release.

## Operational security expectations

Use trusted TLS, read-only connector accounts, narrow CORS, management/VPN/firewall restrictions, non-root services, and protected environment/CA files. Rotate credentials exposed outside their intended location. Use DB-backed bearer identities with the least necessary role. `/health`, `/docs`, `/redoc`, and `/openapi.json` are public by default; apply the management boundary to them as well.

Production rejects fixtures/mock routes and unsafe/incomplete configuration. Tenant-scoped ORM reads/writes and composite relationships protect application access; they are not PostgreSQL RLS or protection from a privileged database administrator. Keep raw SQL restricted to reviewed migration/backup/authentication paths. REAL and TEST data are separated; Replay has no external delivery or execution path.

Keep provider delivery disabled until a reviewed canary. Acknowledged proposals do not execute actions in this release. The source/staged secret scanner is heuristic; review findings and use an additional independent scanner in your own security process. CI must remain independent of live lab credentials.
