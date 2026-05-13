![Project Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=180&section=header&text=port-map-audit&fontSize=50&fontAlignY=38)

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

# port-map-audit

Find local port collisions before Docker, reverse proxies, test servers, and app configs fight over the same socket.

![Code Snippet](assets/code-snapshot.png)

![Terminal Output](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=400&size=14&duration=1500&pause=500&center=false&vCenter=false&multiline=true&width=600&height=200&lines=$+port-map-audit+examples+--fail-on+none;6379+risk+redis+default+port;8080+conflict+port+appears+in+multiple+contexts)

## What It Checks

| Signal | Example | Why it matters |
| --- | --- | --- |
| URLs | `http://localhost:8080` | catches hard-coded service endpoints |
| env assignments | `API_PORT=8080` | finds runtime settings |
| Docker mappings | `"8080:80"` | detects host port reuse |
| listeners | `listen 127.0.0.1:443` | flags proxy/server bindings |

## Install

```bash
git clone https://github.com/mertefekurt/port-map-audit.git
cd port-map-audit
python3 -m pip install .
```

## Usage

```bash
port-map-audit .
port-map-audit ./infra --format json
port-map-audit . --fail-on risk
```

## CLI Reference

| Argument / flag | Default | Purpose |
| --- | ---: | --- |
| `path` | `.` | Directory or file to scan |
| `--format table\|json` | `table` | Human output or machine-readable JSON |
| `--fail-on none\|risk\|conflict` | `conflict` | CI exit policy |
| `--include-hidden` | `false` | Include hidden files and folders |
| `--max-size bytes` | `256000` | Skip very large files |
| `--extension ext` | none | Include extra file extensions |

## Architecture

```mermaid
flowchart TD
    A["CLI arguments"] --> B["scan_path"]
    B --> C["candidate file discovery"]
    C --> D["regex port extraction"]
    D --> E["analyze_hits"]
    E --> F{"finding level"}
    F -->|conflict| G["same port in multiple files or contexts"]
    F -->|risk| H["privileged or common infra port"]
    F -->|clean| I["no findings"]
    G --> J["table or JSON renderer"]
    H --> J
    I --> J
    J --> K["exit policy"]
```

## Project Layout

| Path | Role |
| --- | --- |
| `src/port_map_audit/scanner.py` | file discovery and port extraction |
| `src/port_map_audit/analyzer.py` | conflict and risk classification |
| `src/port_map_audit/renderers.py` | table and JSON output |
| `src/port_map_audit/cli.py` | argparse entrypoint and exit policy |
| `tests/` | unit tests for scanner and CLI policy |

## Test

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
