# Change Predictor

> Know what will break before you change your code.

> AI-powered engineering decision engine for software repositories.


A Python-based repository analysis and change-impact prediction tool that examines code structure, maps dependencies, and estimates which files and symbols may be affected by a change.

It combines AST-based static analysis with Git diff analysis to help developers understand repository structure and assess potential change impact before modifying code.

## ✨ Features

### Repository Analysis
- Repository scanning and Python file discovery
- AST-based Python source parsing
- Class, function, and import extraction
- Dependency graph generation
- Function call graph construction
- Circular dependency detection
- Dead code detection

### Change Impact Analysis
- Git-based change detection
- Added, modified, deleted, and renamed file detection
- Added and deleted line-range extraction
- Changed-symbol mapping
- Direct and transitive dependency impact analysis
- Heuristic risk scoring and impact reporting
- Change simulation

### Reporting and Export
- JSON reports
- Interactive HTML reports
- Markdown reports
- Mermaid dependency graph exports
- PDF reports

---

## 🏗️ Architecture

```text
                    Python Repository
                           |
                           v
                    Repository Scanner
                           |
                           v
                    Python AST Parser
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Symbol Analysis              Dependency Analysis
             |                           |
             v                           v
       Symbol Table                Dependency Graph
             |                           |
             +-------------+-------------+
                           |
                           v
                    Analysis Engine
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
         Call Graph    Cycle/Dead     Impact and
                       Code Analysis  Risk Analysis
                                           |
                                           v
                                    Report Generation

                    Git-Based Analysis
                           |
                           v
                       Git Diff
                           |
                           v
                  Changed File and Line
                       Detection
                           |
                           v
                    Symbol Mapping
                           |
                           v
                  Change Impact Analysis
```

---

## 📂 Project Structure

```text
change-predictor/
|
├── .github/
│   └── workflows/
│       └── tests.yml
|
├── src/
│   └── change_predictor/
│       ├── analysis/
│       ├── analyzer/
│       ├── call_graph/
│       ├── exporters/
│       ├── git_analysis/
│       │   ├── diff_analyzer.py
│       │   ├── line_changes.py
│       │   ├── line_change_parser.py
│       │   ├── symbol_mapper.py
│       │   ├── change_impact_analyzer.py
│       │   └── run_git_impact.py
│       ├── graph/
│       ├── impact/
│       ├── models/
│       ├── reporting/
│       ├── simulation/
│       ├── symbols/
│       └── cli.py
|
├── tests/
│   ├── test_change_impact_analyzer.py
│   └── test_git_line_change_parser.py
|
├── images/
├── .gitignore
└── README.md
```


---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/ApurvaPatil2401/change-predictor.git
cd change-predictor
```

Create and activate a virtual environment:

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the PDF reporting dependency if you intend to generate PDF reports:

```bash
pip install reportlab
```

---

## Usage

The original repository analysis CLI is run from the `src` directory.

```bash
cd src
```

### Analyze a repository

```bash
python -m change_predictor.cli path/to/repository
```

### Analyze the impact of a file

```bash
python -m change_predictor.cli path/to/repository --impact repository.py
```

### Simulate a change

```bash
python -m change_predictor.cli path/to/repository --simulate repository.py
```

### Generate reports

```bash
python -m change_predictor.cli path/to/repository --json
python -m change_predictor.cli path/to/repository --html
python -m change_predictor.cli path/to/repository --markdown
python -m change_predictor.cli path/to/repository --mermaid
python -m change_predictor.cli path/to/repository --pdf
```

### Git-Based Change Impact Analysis (V2)

From the `src` directory, run:

```bash
python -m change_predictor.git_analysis.run_git_impact ..
```

This analyzes Git changes for the target repository using the command's default comparison range.

The Git analysis module identifies changed files, extracts line-level changes, maps changed regions to Python symbols, and produces change-impact information.

---

## Testing

Run the test suite from the repository root:

```bash
python -m pip install pytest anyio
python -m pytest -v
```

The project uses GitHub Actions to run automated tests on pushes to `main` and `feature/git-diff-impact`, and on pull requests targeting `main`.

[View GitHub Actions](https://github.com/ApurvaPatil2401/change-predictor/actions)


## 📊 Sample Output

Repository Summary

```
Python Files : 35
Classes      : 27
Functions    : 50
Imports      : 82
```

Impact Analysis

```
Target File : repository.py

Risk Level : HIGH
Risk Score : 60

Affected Files
---------------
call_graph_builder.py
cli.py
graph_builder.py
symbol_builder.py
```

---
## 📷 Screenshots

### CLI Analysis

Shows repository analysis, dependency graph, circular dependency detection, and dead code detection.

![CLI Analysis](images/cli_analysis.png)

---

### HTML Report

Interactive HTML report generated by the tool.

![HTML Report](images/html_report.png)

---

### Dependency Graph

Mermaid visualization of module dependencies.

![Dependency Graph](images/dependency_graph.png)

---

### PDF Report

Professional PDF summary of repository analysis.

![PDF Report](images/pdf_report.png)
---

## 📄 Reports Generated

- JSON
- HTML
- Markdown
- Mermaid Graph
- PDF

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| AST | Python source-code parsing |
| Git | Change detection and diff analysis |
| Dependency Graphs | Dependency and impact analysis |
| Mermaid | Graph visualization |
| HTML/CSS | HTML reporting |
| ReportLab | PDF generation |
| pytest | Automated testing |
| GitHub Actions | Continuous integration |

---

## Current Limitations

- Python-focused static analysis.
- Impact and risk estimates are heuristic, not guarantees of runtime behavior.
- Symbol mapping is based on available source-code information.
- Git-based analysis requires a Git repository and accessible comparison history.

---

## 📌 Future Improvements

- Enhanced cross-file symbol resolution
- More precise rename and deleted-symbol analysis
- Improved risk scoring
- Interactive dependency visualization
- Multi-language support
- IDE integration

---

## Project Goal

The goal of Change Predictor is to make software changes easier to reason about by identifying potentially affected parts of a codebase before changes are introduced.

**Understand dependencies. Predict impact. Make safer changes.**
---