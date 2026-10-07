"""Read-only static release checks; no database, provider calls, or credentials required."""
import ast
import importlib.metadata as metadata
import json
from pathlib import Path
import re
import sys

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    files = [p for p in root.rglob('*') if p.is_file() and not any(
        part in {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache'} for part in p.relative_to(root).parts)]
    for path in files:
        if path.suffix == '.py':
            try:
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path.relative_to(root)))
            except SyntaxError:
                errors.append(f'Invalid Python syntax: {path.relative_to(root)}')
        if path.suffix == '.md':
            # Local file links; web URLs, anchors and code examples are excluded.
            content = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
                if '://' in target or target.startswith(('#', 'mailto:')):
                    continue
                target = target.split('#')[0]
                if target and not (path.parent / target).exists():
                    errors.append(f'Broken documentation link: {path.relative_to(root)} -> {target}')
    pins = {}
    for line in (root/'requirements.lock.txt').read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        req = Requirement(line)
        if not req.marker or req.marker.evaluate():
            pins[canonicalize_name(req.name)] = req
            try:
                if metadata.version(req.name) not in req.specifier:
                    errors.append(f'Installed dependency differs from lock: {req.name}')
            except metadata.PackageNotFoundError:
                errors.append(f'Missing locked dependency: {req.name}')
    for line in (root/'requirements.txt').read_text().splitlines():
        if not line.strip() or line.startswith(('#','-')):
            continue
        req = Requirement(line)
        pin = pins.get(canonicalize_name(req.name))
        if not pin or metadata.version(req.name) not in req.specifier:
            errors.append(f'Direct requirement/lock mismatch: {req.name}')
    values = {}
    for line in (root/'.env.example').read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            values[key] = value
    for key in ('POSTGRES_PASSWORD','AUTH_TOKENS','SPLUNK_TOKEN','WAZUH_PASSWORD','CRYPTOGUARD_READ_KEY',
                'TELEGRAM_BOT_TOKEN','SMS_WEBHOOK_TOKEN','TELEGRAM_CHAT_ID','SMS_TO','TEST_TELEGRAM_CHAT_ID'):
        if values.get(key):
            errors.append(f'.env.example must leave {key} empty')
    if 'CHANGE_ME' not in values.get('DATABASE_URL',''):
        errors.append('DATABASE_URL must contain a password placeholder')
    for key in ('ALLOW_FIXTURES','ENABLE_LEGACY_MOCK_ROUTES','TELEGRAM_ENABLED','SMS_ENABLED','ALLOW_TEST_NOTIFICATIONS'):
        if values.get(key) != 'false':
            errors.append(f'Unsafe example default: {key}')
    compose = yaml.safe_load((root/'docker-compose.yml').read_text())
    backend = compose['services']['backend']
    if backend.get('build') != '.' or '127.0.0.1:8003:8003' not in backend.get('ports', []):
        errors.append('Compose build path or loopback binding changed')
    if not backend.get('read_only') or backend.get('user') != '10001:10001':
        errors.append('Compose runtime hardening changed')
    dockerfile = (root/'Dockerfile').read_text()
    if 'COPY requirements.lock.txt .' not in dockerfile or 'USER sentinelzone' not in dockerfile:
        errors.append('Dockerfile release paths/user changed')
    # GitHub resolves workflow paths from the standalone repository root.
    workflow_path = root/'.github/workflows/backend-ci.yml'
    if not workflow_path.is_file():
        errors.append('Missing repository-root GitHub Actions workflow')
    else:
        workflow = yaml.load(workflow_path.read_text(), Loader=yaml.BaseLoader)
        if not {'push', 'pull_request', 'workflow_dispatch'} <= set(workflow.get('on', {})):
            errors.append('Missing expected CI triggers')
        for name in ('sqlite', 'postgresql'):
            job = workflow.get('jobs', {}).get(name, {})
            if job.get('defaults', {}).get('run', {}).get('working-directory', '.') != '.':
                errors.append(f'CI job must run from repository root: {name}')
            setup = [s for s in job.get('steps', []) if s.get('uses', '').startswith('actions/setup-python@')]
            if len(setup) != 1 or setup[0].get('with', {}).get('cache-dependency-path') != 'requirements.lock.txt':
                errors.append(f'CI dependency cache path invalid: {name}')
            if not any('python scripts/acceptance.py' in s.get('run', '') for s in job.get('steps', [])):
                errors.append(f'CI acceptance command missing: {name}')
    if (root/'backend').exists():
        errors.append('Unexpected nested backend directory in standalone release')
    for required in ('PUSH_TO_GITHUB.md', 'RELEASE_MANIFEST.md', 'LICENSE-TODO.md', 'THIRD_PARTY_NOTICES.md'):
        if not (root/required).is_file():
            errors.append(f'Missing root release file: {required}')
    api = json.loads((root/'docs/openapi.json').read_text())
    if any(path.startswith('/api/') for path in api['paths']):
        errors.append('Legacy mock routes leaked into default contract')
    operations = sum(k in {'get','put','post','delete','patch','head','options'} for v in api['paths'].values() for k in v)
    result = {'status': 'FAIL' if errors else 'PASS', 'api_paths': len(api['paths']),
              'api_operations': operations, 'active_locked_distributions': len(pins), 'errors': errors}
    return result


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, indent=2))
    sys.exit(bool(result['errors']))
