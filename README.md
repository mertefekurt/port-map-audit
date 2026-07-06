![Port Map Audit cover](assets/readme-cover.svg)

# Port Map Audit

Scan project configs for local port conflicts and risky bindings.

## Working shape

The repo is meant to be opened, understood, and run quickly. The command surface is deliberately narrow: `port-map-audit`.

## Fresh clone

```bash
git clone https://github.com/mertefekurt/port-map-audit.git
cd port-map-audit
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## First command

```bash
port-map-audit examples/docker-compose.yml
```

## Local confidence

```bash
ruff check .
pytest
python -m port_map_audit --help
```
