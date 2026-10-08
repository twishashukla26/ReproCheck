from reprocheck.repository import (
    check_readme,
    check_license,
    check_dependencies
)

from reprocheck.dependencies import read_dependencies
from reprocheck.import_checker import find_imports
from reprocheck.file_checker import check_file_exists, check_absolute_paths
from reprocheck.dependency_checker import check_dependency_mismatches
from reprocheck.docker_checker import (
    check_docker_files,
    check_dockerfile_structure
)

from reprocheck.json_report import (
    collect_results,
    save_json_report
)

from reprocheck.result import CheckResult
from reprocheck.report import format_report

import sys


def build_check_results(project_path):

    results = []

    # Repository checks
    if check_readme(project_path):
        results.append(
            CheckResult(
                "README",
                "PASS",
                "README found"
            )
        )
    else:
        results.append(
            CheckResult(
                "README",
                "FAIL",
                "README file missing"
            )
        )

    if check_license(project_path):
        results.append(
            CheckResult(
                "LICENSE",
                "PASS",
                "LICENSE found"
            )
        )
    else:
        results.append(
            CheckResult(
                "LICENSE",
                "WARNING",
                "LICENSE file missing"
            )
        )

    if check_dependencies(project_path):
        results.append(
            CheckResult(
                "Dependencies",
                "PASS",
                "Dependencies file found"
            )
        )
    else:
        results.append(
            CheckResult(
                "Dependencies",
                "WARNING",
                "Dependencies file missing"
            )
        )

    # Dependency mismatch check
    mismatches = check_dependency_mismatches(project_path)

    if mismatches:
        results.append(
            CheckResult(
                "Dependency Mismatches",
                "WARNING",
                f"{len(mismatches)} imported package(s) not declared"
            )
        )
    else:
        results.append(
            CheckResult(
                "Dependency Mismatches",
                "PASS",
                "No dependency mismatches detected"
            )
        )

    # Required data file
    sample_file = "data/sample.csv"

    if check_file_exists(project_path, sample_file):
        results.append(
            CheckResult(
                "Sample Data",
                "PASS",
                f"{sample_file} found"
            )
        )
    else:
        results.append(
            CheckResult(
                "Sample Data",
                "FAIL",
                f"{sample_file} missing"
            )
        )

    # Hard-coded absolute paths
    absolute_paths = check_absolute_paths(project_path)

    if absolute_paths:
        results.append(
            CheckResult(
                "Hard-coded Paths",
                "WARNING",
                f"{len(absolute_paths)} absolute path(s) detected"
            )
        )
    else:
        results.append(
            CheckResult(
                "Hard-coded Paths",
                "PASS",
                "No hard-coded absolute paths detected"
            )
        )

    # Docker checks
    docker_results = check_docker_files(project_path)

    if docker_results["Dockerfile"]:
        results.append(
            CheckResult(
                "Dockerfile",
                "PASS",
                "Dockerfile found"
            )
        )

        dockerfile_structure = check_dockerfile_structure(project_path)

        if dockerfile_structure["valid"]:
            results.append(
                CheckResult(
                    "Dockerfile Structure",
                    "PASS",
                    "Dockerfile structure valid"
                )
            )
        else:
            missing = ", ".join(dockerfile_structure["missing"])

            results.append(
                CheckResult(
                    "Dockerfile Structure",
                    "WARNING",
                    f"Dockerfile structure incomplete; missing: {missing}"
                )
            )

    else:
        results.append(
            CheckResult(
                "Dockerfile",
                "FAIL",
                "Dockerfile missing"
            )
        )

    if docker_results["Docker Compose"]:
        results.append(
            CheckResult(
                "Docker Compose",
                "PASS",
                "Docker Compose file found"
            )
        )
    else:
        results.append(
            CheckResult(
                "Docker Compose",
                "WARNING",
                "Docker Compose file missing"
            )
        )

    return results


def generate_report(project_path):

    results = build_check_results(project_path)

    print(format_report(project_path, results))

    print("\nDeclared Dependencies:")

    dependencies = read_dependencies(project_path)

    for dependency in dependencies:
        print("-", dependency)

    print("\nDetected Imports:")

    imports = find_imports(project_path)

    for package in imports:
        print("-", package)


def main():

    if len(sys.argv) < 2:
        print("Please provide project path")
        return

    project_path = sys.argv[1]

    generate_report(project_path)

    if "--json" in sys.argv:
        results = collect_results(project_path)

        save_json_report(
            project_path,
            results,
            "report.json"
        )

        print("\n✓ JSON report saved to report.json")


if __name__ == "__main__":
    main()