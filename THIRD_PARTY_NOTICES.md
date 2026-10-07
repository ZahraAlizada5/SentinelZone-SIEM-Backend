# Third-party dependencies and notices

This source ZIP does not vendor dependency wheels, site-packages, private certificates, or external source trees. It references packages through the retained dependency lock. Those packages are independently licensed; any future project license applies only to code the owner has the right to license.

[docs/DEPENDENCY_LICENSES.md](docs/DEPENDENCY_LICENSES.md) records names, exact versions, declared license metadata, and installed license-file locations from the environment used for validation. This is an inventory, not a determination of legal compatibility. Preserve each dependency's actual license and notices when redistributing a built container, wheel bundle, executable or modified dependency.

Pay particular attention to psycopg/psycopg-binary (declared LGPL-3.0-only), certifi (MPL 2.0), typing_extensions (PSF-2.0), and packages with multiple declared licenses such as uvloop. Binary packages may contain additional components with separate notices; the package-level table is not a complete binary SBOM. Docker base image and PostgreSQL image contents have their own terms.

The existing fixture payloads include sensor names and a Suricata signature label; no rule corpus or third-party application is bundled. Fixture provenance/redistribution rights should be confirmed by the owner along with original code ownership. The historical audit documentation is retained without granting new rights.

No original project license was supplied. See [LICENSE-TODO.md](LICENSE-TODO.md).
