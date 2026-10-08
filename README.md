# ReproCheck

### An Open-Source Reproducibility Auditor for Data Science and Software Projects

ReproCheck is a lightweight open-source tool that audits a Python-based software or data science project for common reproducibility issues.

It checks whether important project files, dependencies, referenced files, paths, and container configuration are present and consistent. The tool produces a structured report so that another user can identify potential problems before attempting to reproduce the project.

---

## Problem Statement

A software or data science project may contain source code, datasets, dependencies, and documentation, but these files do not always guarantee that another user can successfully run the project on a different machine.

Common reproducibility problems include:

- Missing README or license files
- Missing dependency declarations
- Imported Python packages not declared as dependencies
- Missing referenced files
- Hard-coded absolute paths
- Missing Docker configuration
- Incomplete Dockerfile instructions

ReproCheck aims to automatically identify these common issues and generate a reproducibility report.

---

## Objectives

The main objectives of ReproCheck are to:

- Inspect the structure of a project repository.
- Check for important documentation and configuration files.
- Read and analyse Python dependencies.
- Detect imported packages that are not declared.
- Detect missing referenced files.
- Detect hard-coded absolute paths.
- Check Docker and Docker Compose configuration.
- Generate structured JSON results.
- Provide a reproducible execution environment using Docker.
- Present findings using PASS, WARNING, and FAIL statuses.

---

## Workflow

```text
                    Target Project
                         |
                         v
                  Project Scanner
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 Repository         Dependency       File & Path
   Checks             Checks            Checks
        |                |                |
        +----------------+----------------+
                         |
                         v
                   Docker Checks
                         |
                         v
                 Structured Results
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Terminal Report          JSON Report
Checks Performed
1. Repository Checks

ReproCheck checks for important project files:

README.md, README.txt, or README
LICENSE, LICENSE.txt, or LICENSE.md
requirements.txt or pyproject.toml
2. Dependency Checks

The tool:

Reads dependencies from requirements.txt.
Detects Python imports using the Python AST module.
Compares imported packages with declared dependencies.
Reports packages that are imported but not declared.
3. File and Path Checks

ReproCheck checks whether expected project files exist.

It also scans Python files for common hard-coded absolute paths such as:

C:\Users\...
/home/...
/Users/...

These paths can prevent a project from working on another machine.

4. Docker Checks

The tool checks for:

Dockerfile
docker-compose.yml
docker-compose.yaml

It also validates basic Dockerfile instructions including:

FROM
WORKDIR
COPY
RUN
CMD
5. Structured PASS / WARNING / FAIL Reporting

Each check produces a structured result containing:

Check name
Status
Message

The report groups findings into:

PASSED
WARNINGS
FAILED

This makes it easier to distinguish successful checks from potential reproducibility problems and missing required components.

6. JSON Reporting

ReproCheck can generate a structured JSON report containing project check results and analysis information.

Run:

python -m reprocheck.main benchmark_projects/project_docker --json

The generated report.json can be used by other tools or workflows.

Technology Stack
Technology	Purpose
Python	Core implementation
pathlib	File and directory handling
ast	Python import analysis
re	Absolute path detection
json	Structured report generation
pytest	Automated testing
Git	Version control
GitHub	Open-source repository
Docker	Containerization
Docker Compose	Reproducible execution workflow
Git Bash	Development environment
Project Structure
ReproCheck/
│
├── benchmark_projects/
│   ├── project_clean/
│   ├── project_missing_dependency/
│   ├── project_hardcoded_path/
│   └── project_docker/
│
├── reprocheck/
│   ├── __init__.py
│   ├── scanner.py
│   ├── repository.py
│   ├── dependencies.py
│   ├── import_checker.py
│   ├── dependency_checker.py
│   ├── file_checker.py
│   ├── docker_checker.py
│   ├── json_report.py
│   ├── result.py
│   ├── report.py
│   └── main.py
│
├── tests/
│   ├── test_scanner.py
│   ├── test_repository.py
│   ├── test_dependencies.py
│   ├── test_import_checker.py
│   ├── test_dependency_checker.py
│   ├── test_file_checker.py
│   ├── test_docker_checker.py
│   ├── test_json_report.py
│   ├── test_report.py
│   └── test_main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
Installation

Clone the repository:

git clone https://github.com/twishashukla26/ReproCheck.git
cd ReproCheck

Create a virtual environment:

Windows Git Bash
python -m venv .venv
source .venv/Scripts/activate

Install dependencies:

pip install -r requirements.txt
Basic Usage

Run ReproCheck against a benchmark project:

python -m reprocheck.main benchmark_projects/project_clean

The tool prints a structured reproducibility report in the terminal.

Example
========================================
        REPROCHECK REPORT
========================================

Project: benchmark_projects/project_clean

PASSED
------
  ✓ README: README found
  ✓ LICENSE: LICENSE found
  ✓ Dependencies: Dependencies file found
  ✓ Dependency Mismatches: No dependency mismatches detected
  ✓ Sample Data: data/sample.csv found
  ✓ Hard-coded Paths: No hard-coded absolute paths detected

WARNINGS
--------
  ⚠ Docker Compose: Docker Compose file missing

FAILED
------
  ✗ Dockerfile: Dockerfile missing

----------------------------------------
Summary
-------
Passed:   6
Warnings: 1
Failed:   1
----------------------------------------

The exact results depend on the project being analysed.
Understanding the Statuses
PASS

The check was successfully satisfied.

Example:

✓ Dependencies: Dependencies file found
WARNING

A potential reproducibility issue was detected, but the project may still contain enough information to continue analysis.

Example:

⚠ Dependency Mismatches: 1 imported package(s) not declared
FAIL

A required component or condition was not satisfied.

Example:

✗ Sample Data: data/sample.csv missing

The status classification is based on the current ReproCheck implementation and is intended to make the report easier to interpret.

JSON Report

To generate a JSON report:

python -m reprocheck.main benchmark_projects/project_docker --json

The command generates:

report.json

The JSON output provides structured results that can be used by other tools or workflows.

Running with Docker

Build the ReproCheck Docker image:

docker compose build

Run the project:

docker compose up

ReproCheck can also be run against a benchmark project inside the container:

docker compose run --rm reprocheck python -m reprocheck.main benchmark_projects/project_docker

Example Docker checks:

✓ Dockerfile: Dockerfile found
✓ Dockerfile Structure: Dockerfile structure valid
✓ Docker Compose: Docker Compose file found
Benchmark Projects

ReproCheck includes small benchmark projects with controlled conditions for testing the auditor.

Benchmark	Purpose
project_clean	Demonstrates a project with basic required files and dependencies
project_missing_dependency	Tests detection of undeclared Python imports
project_hardcoded_path	Tests detection of hard-coded absolute paths
project_docker	Tests Dockerfile and Docker Compose checks

These benchmark projects allow the behaviour of ReproCheck to be tested without depending on external repositories.

Testing

Run the complete automated test suite:

python -m pytest

Current test result:

18 passed

The tests cover:

Project scanning
Repository checks
Dependency reading
Import detection
Dependency mismatch detection
File checks
Hard-coded path detection
Docker checks
JSON reporting
Structured report formatting
Main CLI workflow
Scope and Limitations
Included
Python-based software and data science projects
Repository structure checks
Dependency analysis
Python import analysis
File and path checks
Docker configuration checks
JSON reporting
PASS / WARNING / FAIL reporting
Automated testing
Containerized execution
Not Included

ReproCheck does not attempt to:

Automatically fix detected problems
Guarantee that every external project can be reproduced
Replace CI/CD systems
Perform a complete security audit
Deploy projects to the cloud
Support every programming language

The tool focuses on identifying common reproducibility issues.

Reproducibility

ReproCheck itself is designed to be reproducible.

A new user can:

Clone the GitHub repository.
Install the listed dependencies.
Run the automated tests.
Run ReproCheck against a benchmark project.
Build and run the Docker container.

This provides multiple ways to verify that the project works in another environment.

Open-Source License

This project is released under the MIT License.

See LICENSE for the complete license text.

Project Status

The core ReproCheck workflow is implemented and tested.

Current implementation includes:

Repository auditing
Dependency analysis
Import analysis
File and path checks
Docker checks
Structured PASS / WARNING / FAIL reporting
JSON reporting
Automated tests
Docker Compose execution

The project is intended as a lightweight reproducibility auditing tool rather than a complete automated reproduction system.
