from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.model_factory import create_adapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--adapter', default='heuristic')
    parser.add_argument('--endpoint', default=None)
    parser.add_argument('--model', default=None)
    parser.add_argument('--require-live-backend', action='store_true')
    parser.add_argument('--smoke-prompt', default='Reply with the single word READY.')
    args = parser.parse_args()

    build_kwargs = {}
    if args.endpoint:
        build_kwargs['endpoint'] = args.endpoint
    if args.model:
        build_kwargs['model'] = args.model

    adapter = create_adapter(args.adapter, **build_kwargs)
    health = adapter.healthcheck()
    smoke = None
    ok = bool(health.get('ok'))
    if ok:
        if hasattr(adapter, 'smokecheck'):
            smoke = adapter.smokecheck(prompt=args.smoke_prompt)
        else:
            response = adapter.generate(args.smoke_prompt, system_prompt='You are a backend smokecheck agent.')
            smoke = {'ok': response.ok and bool(response.text.strip()), 'text': response.text[:120], 'error': response.error, 'latency_ms': response.latency_ms}
        ok = ok and bool(smoke.get('ok'))

    if args.require_live_backend and getattr(adapter, 'promotable', True) is False:
        ok = False
        if smoke is None:
            smoke = {}
        smoke['error'] = 'Synthetic baseline adapter does not satisfy require-live-backend.'

    payload = {
        'ok': ok,
        'adapter': args.adapter,
        'identity': adapter.backend_identity(),
        'health': health,
        'smoke': smoke,
        'require_live_backend': args.require_live_backend,
    }
    print(json.dumps(payload, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
