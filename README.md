# Port Map Audit

![Port Map Audit cover](assets/readme-cover.svg)

![stack](https://img.shields.io/badge/stack-Python-7c3aed?style=flat-square) ![python](https://img.shields.io/badge/python-3.9-0891b2?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-b45309?style=flat-square) ![tests](https://img.shields.io/badge/tests-pytest-be185d?style=flat-square)

> Scan project configs for local port conflicts and risky bindings

## How I use it

The project stays focused on one job: take a small input, produce a clear result, and avoid adding a heavy service around a problem that fits in a command line.

## Quick start

```bash
python -m pip install -e ".[dev]"
port-map-audit examples/docker-compose.yml
```

## What is inside

```text
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m port_map_audit --help
```
