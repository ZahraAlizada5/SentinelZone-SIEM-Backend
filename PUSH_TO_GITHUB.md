# Publish SentinelZone-SIEM-Backend to GitHub

This package is a complete standalone repository. Its destination is your own **SentinelZone-SIEM-Backend** repository. It does not require a Pull Request into the separate SentinelZone-SOC-Platform integration repository.

Extract the ZIP and open `SentinelZone-SIEM-Backend/`. Read [README.md](README.md), [release status](docs/STATUS.md), and [known limitations](docs/KNOWN_LIMITATIONS.md). Include dotfiles when transferring the package. No extra source directory needs to be created. Resolve [LICENSE-TODO.md](LICENSE-TODO.md) before granting unrestricted reuse; publishing source alone does not grant an open-source license.

## Before either workflow

Verify the ZIP against its adjacent `.zip.sha256` file, then verify the extracted source **before** tests refresh reports. On Linux:

```bash
# Run beside the ZIP and its checksum file:
sha256sum -c SentinelZone-SIEM-Backend-v0.28.1.zip.sha256
cd SentinelZone-SIEM-Backend
sha256sum -c SHA256SUMS
```

From the repository root, with CPython 3.12 installed:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pip check
python scripts/acceptance.py
python scripts/export_contracts.py --check
python scripts/check_secrets.py
python scripts/validate_release.py
```

Use Linux/WSL2 for full acceptance. On native Windows, see [INSTALL.md](INSTALL.md) for environment setup; native platform acceptance remains UNVERIFIED. Run validation before creating a deployment `.env`. Tests use synthetic data and temporary databases; no real provider credentials are needed.

**Before `git add`, run the secret scan and confirm there are no real `.env` files, private keys, tokens, passwords, databases, logs, backups, or runtime artifacts to stage.** Keep the placeholder-only `.env.example`. Review ignored files with `git status --short --ignored`; `.gitignore` is not a substitute for inspection. After staging, scan the actual index again.

The supplied root `.github/workflows/backend-ci.yml` is already in the correct location. It runs on pushes and pull requests, with no live lab credentials. Local equivalent SQLite acceptance is measured; GitHub-hosted and PostgreSQL job execution remain UNVERIFIED.

## A. Create a new standalone repository

1. In GitHub, create a new repository named **SentinelZone-SIEM-Backend** under your account or authorized organization. Leave it empty: do not initialize a README, license, or `.gitignore`. Choose visibility deliberately; a license decision is still required for unrestricted reuse.
2. Open a terminal in the extracted `SentinelZone-SIEM-Backend/` directory. Complete the validation above.
3. Replace `USERNAME` below with the actual GitHub owner. If Git needs your identity, configure your own `user.name` and `user.email` first.

```bash
git init
git branch -M main
git status --short --ignored
python scripts/check_secrets.py
git add .
python scripts/check_secrets.py --staged
git diff --cached --stat
git diff --cached
git commit -m "Initial SentinelZone SIEM Backend release"
git remote add origin https://github.com/USERNAME/SentinelZone-SIEM-Backend.git
git push -u origin main
```

Stop and remove any unintended staged content before committing. Do not bypass a scanner finding without reviewing it. Use GitHub's normal credential manager, SSH setup, or browser authentication; never put a token in the remote URL or commit a credential file.

After the push, inspect the GitHub file tree and Actions results. Do not report hosted CI as passing until its actual jobs succeed. Enable a private vulnerability-reporting channel and appropriate branch protection in your repository settings.

## B. Update an existing standalone repository

Use a clean checkout and preserve any newer work. Replace `USERNAME` with the repository owner:

```bash
git clone https://github.com/USERNAME/SentinelZone-SIEM-Backend.git
cd SentinelZone-SIEM-Backend
git status --short
git switch main
git pull --ff-only
git switch -c chore/standalone-release
```

If `git status` shows local changes, resolve them before proceeding. Compare the extracted package with the checkout, then copy its **contents**, including dotfiles, into the checkout root. Preserve the checkout's `.git/`; do not delete unrelated/newer work. Do not copy a deployment `.env`, database, or virtual environment. Reconcile conflicts instead of blindly overwriting concurrent changes. The supplied package contains no `.git/`.

Set up the Python environment and repeat the validation in “Before either workflow.” Then:

```bash
git status --short --ignored
python scripts/check_secrets.py
git add .
python scripts/check_secrets.py --staged
git diff --cached --stat
git diff --cached
git commit -m "Prepare standalone SentinelZone SIEM Backend release"
git push -u origin chore/standalone-release
```

Open a Pull Request from `chore/standalone-release` into `main` in **this standalone repository**. Include measured test/acceptance results and every remaining UNVERIFIED gate. If you lack write access, fork this standalone repository, clone your fork, follow the same branch workflow, and open the PR back to its owner. Follow the owner's review/merge policy.

## Release evidence

[RELEASE_MANIFEST.md](RELEASE_MANIFEST.md) explains the package layout and source checksums. The external manifest supplied beside the ZIP records its exact SHA-256 and the acceptance run from a fresh extraction. Running tests refreshes reports, so shipped source checksums will then differ for those evidence files; review those changes before committing. Changing source content for another release requires new checksums and another clean extraction test.
