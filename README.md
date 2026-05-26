# Context Aware Copilot Toolkit

> AI-powered code review and completion engine with semantic diff analysis using Xiaomi MiMo for actionable suggestions.

`code-review` `ai-copilot` `mimo` `developer-tools`

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with MiMo](https://img.shields.io/badge/Built%20with-Xiaomi%20MiMo-orange.svg)](https://platform.xiaomimimo.com)

## Overview

`context-aware-copilot-toolkit` is built on top of [Xiaomi MiMo](https://platform.xiaomimimo.com), the open-source large language model series from Xiaomi. The project demonstrates how to integrate MiMo into production systems using its OpenAI-compatible API.

## Use Cases

- **Pre-merge code review** — surface issues before reviewers see the PR
- **Refactoring suggestions** — identify duplication and complexity hotspots
- **Onboarding help** — explain unfamiliar code to new contributors
- **Security scanning** — catch common vulnerabilities (injection, auth bypass)

## Quick Start

### Install

```bash
pip install -e .
# or for development
pip install -e ".[dev]"
```

### Run

```bash
export MIMO_API_KEY=your_key_here
python main.py
```

### Programmatic Use

```python
import asyncio
from context_aware_copilot_toolkit.client import MiMoClient

async def example():
    client = MiMoClient(model="mimo-7b", api_key="...")
    response = await client.chat("Hello, MiMo!")
    print(response["content"])

asyncio.run(example())
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Application │───▶│  context_aware_ │───▶│  Xiaomi MiMo    │
│              │     │  (this repo) │     │  (LLM API)      │
└─────────────┘     └──────────────┘     └─────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Local State │
                    │  / Cache     │
                    └──────────────┘
```

The library wraps the MiMo HTTP API and exposes a high-level interface tuned for the code assist use case. Configuration is YAML-first with environment variable overrides for secrets.

## Configuration

`config.yaml`:

```yaml
model: ${MIMO_MODEL:-mimo-7b}
api_key: ${MIMO_API_KEY}
max_parallel: 4
```

Environment variables override file values. See `config.yaml` in the repo root for the full schema.

## Development

```bash
# Run tests
pytest -v

# Lint
ruff check .
```

CI runs on every push and PR via GitHub Actions (`.github/workflows/ci.yml`).

## Project Structure

```
context-aware-copilot-toolkit/
├── README.md
├── LICENSE
├── pyproject.toml
├── config.yaml
├── main.py
├── src/context_aware_copilot_toolkit/
│   ├── reviewer.py
│   ├── client.py
│   └── config.py
├── tests/
│   └── test_reviewer.py
└── .github/
    └── workflows/
        └── ci.yml
```

## Why MiMo?

Xiaomi MiMo is a strong open-weight LLM with competitive reasoning performance and an OpenAI-compatible API. Choosing MiMo as the backend gives this project:

- **Cost-effective inference** — significantly cheaper than proprietary frontier models for comparable quality
- **Open licensing** — weights and code are available under permissive terms
- **Strong reasoning** — competitive performance on math, code, and multi-step planning benchmarks
- **Production-ready API** — drop-in replacement for OpenAI client libraries

## Contributing

Contributions welcome. Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Add tests for new behavior
4. Open a PR with a clear description

See `.github/workflows/ci.yml` for the checks that must pass.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

Built with [Xiaomi MiMo](https://platform.xiaomimimo.com). This project is part of the MiMo 100T Token Plan ecosystem submission.
