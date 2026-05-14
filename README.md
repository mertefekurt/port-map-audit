<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=250&section=header&text=port-map-audit&fontSize=60&fontAlignY=35&desc=Find%20local%20port%20collisions%20before%20Docker%2C%20reverse%20proxies%2C%20test%20servers%2C%20and%20config%20files%20fight%20over%20the%20same%20socket.%20Scan%20your%20project%20for%20risky%20bindings%2C%20duplicate%20host%20ports%2C%20and%20infra-default%20landmines%20with%20a%20CI-ready%20Python%20CLI.&descAlignY=55&descSize=20)

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Detects-Docker%20Maps-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Networking](https://img.shields.io/badge/Focus-Port%20Conflicts-FF4ECD?style=for-the-badge&logo=nginx&logoColor=white)
![CI](https://img.shields.io/badge/CI-Fail%20Policies-16A34A?style=for-the-badge&logo=githubactions&logoColor=white)

</div>

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=33C9FF&width=650&height=40&lines=Port+Maps+Without+The+Guesswork)

`port-map-audit` scans project files for URLs, environment assignments, Docker host mappings, and listener directives that mention local ports. It turns scattered configuration into a clear conflict report so development stacks fail in review instead of at runtime.

<table>
  <tr>
    <td width="50%" valign="top">

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=FF4ECD&width=500&height=40&lines=Core+Features)

- 🔌 Finds duplicate ports across config files and contexts
- 🐳 Detects Docker Compose and Dockerfile-style host mappings
- 🌐 Extracts ports from HTTP, WebSocket, TCP, and UDP URLs
- ⚠️ Flags privileged ports and common infra defaults
- 🧾 Renders human tables or machine-readable JSON
- 🚦 Supports CI exit policies for risk or conflict thresholds

  </td>
  <td width="50%" valign="top">

![Code Snapshot](assets/code-snapshot.png)

  </td>
  </tr>
</table>

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=9DFF57&width=650&height=40&lines=Blazing+Fast+CLI+Demo)

![Demo](https://readme-typing-svg.demolab.com/?font=Fira+Code&duration=1500&pause=500&multiline=true&width=950&height=150&color=F8F8F2&background=282A3600&lines=%24+port-map-audit+.%3B%3E+8080+conflict+port+appears+in+multiple+files+or+contexts%3B%24+port-map-audit+.%2Finfra+--format+json%3B%3E+machine-readable+audit+ready+for+CI)

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=FFB86C&width=650&height=40&lines=Audit+Pipeline)

```mermaid
flowchart TD
    A[CLI Target Path] --> B[Candidate File Discovery]
    B --> C[Skip Hidden, Cache, Build, and Large Files]
    C --> D[Regex Port Extraction]
    D --> E[Group Hits By Port]
    E --> F{Classification}
    F -->|Multiple Files or Contexts| G[Conflict Finding]
    F -->|Privileged or Infra Default| H[Risk Finding]
    F -->|No Signal| I[Clean Port]
    G --> J[Table or JSON Renderer]
    H --> J
    I --> J
    J --> K[Exit Policy]
    classDef input fill:#33C9FF,stroke:#0F172A,color:#0F172A,stroke-width:2px
    classDef scan fill:#9DFF57,stroke:#17320E,color:#0F172A,stroke-width:2px
    classDef classify fill:#FF4ECD,stroke:#2A0A1F,color:#FFFFFF,stroke-width:2px
    classDef output fill:#FFB86C,stroke:#4A2500,color:#0F172A,stroke-width:2px
    classDef danger fill:#EF4444,stroke:#450A0A,color:#FFFFFF,stroke-width:2px
    class A input
    class B,C,D,E scan
    class F classify
    class G danger
    class H,I,J,K output
```

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=33C9FF&width=650&height=40&lines=Quick+Start)

```bash
git clone https://github.com/mertefekurt/port-map-audit.git
cd port-map-audit
python3 -m pip install .
port-map-audit .
```

<details>
<summary>🛠️ View CLI Reference / Advanced Config</summary>

| Command | Purpose |
| --- | --- |
| `port-map-audit .` | Scan the current project and print a table |
| `port-map-audit ./infra --format json` | Scan infrastructure files and emit JSON |
| `port-map-audit . --fail-on risk` | Exit non-zero when risks or conflicts are present |
| `port-map-audit . --include-hidden` | Include hidden files and folders in discovery |

| Flag | Default | Purpose |
| --- | ---: | --- |
| `path` | `.` | Directory or file to scan |
| `--format table\|json` | `table` | Choose human or machine output |
| `--fail-on none\|risk\|conflict` | `conflict` | Select the CI failure threshold |
| `--include-hidden` | `false` | Include dotfiles and hidden folders |
| `--max-size <bytes>` | `256000` | Skip files larger than this value |
| `--extension <ext>` | none | Add an extra extension to scan, repeatable |

| Signal | Example |
| --- | --- |
| URL ports | `http://localhost:8080` |
| Environment assignments | `API_PORT=8080` |
| Docker mappings | `"8080:80"` |
| Listener directives | `listen 127.0.0.1:443` |

</details>

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=FF4ECD&width=650&height=40&lines=Project+Map)

```text
port-map-audit/
├── src/port_map_audit/
│   ├── cli.py        # argparse entrypoint and exit policy
│   ├── scanner.py    # file discovery and port extraction
│   ├── analyzer.py   # conflict and risk classification
│   ├── renderers.py  # table and JSON output
│   └── models.py     # report and finding data structures
├── examples/
├── tests/
└── assets/
    └── code-snapshot.png
```

![Header](https://readme-typing-svg.demolab.com/?font=Righteous&weight=700&size=26&color=9DFF57&width=650&height=40&lines=License)

MIT
