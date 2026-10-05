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

import sys


def generate_report(project_path):

    print("\n===== ReproCheck Report =====\n")

    print("Repository Checks:")

    print(
        "✓ README found"
        if check_readme(project_path)
        else "✗ README missing"
    )

    print(
        "✓ LICENSE found"
        if check_license(project_path)
        else "✗ LICENSE missing"
    )

    print(
        "✓ Dependencies file found"
        if check_dependencies(project_path)
        else "✗ Dependencies file missing"
    )

    print("\nDeclared Dependencies:")

    dependencies = read_dependencies(project_path)

    for dependency in dependencies:
        print("-", dependency)

    print("\nDetected Imports:")

    imports = find_imports(project_path)

    for package in imports:
        print("-", package)

    print("\nDependency Issues:")

    mismatches = check_dependency_mismatches(project_path)

    if mismatches:
        for package in mismatches:
            print("⚠", package, "imported but not declared")
    else:
        print("✓ No dependency mismatches detected")

    print("\nFile Checks:")

    sample_file = "data/sample.csv"

    if check_file_exists(project_path, sample_file):
        print("✓", sample_file, "found")
    else:
        print("✗", sample_file, "missing")

    print("\nHard-coded Paths:")

    absolute_paths = check_absolute_paths(project_path)

    if absolute_paths:
        for file_path, line_number, line in absolute_paths:
            print(
                "⚠ Absolute path detected:",
                file_path,
                "line",
                line_number
            )
    else:
        print("✓ No hard-coded absolute paths detected")

    print("\nDocker Checks:")

    docker_results = check_docker_files(project_path)

    if docker_results["Dockerfile"]:
        print("✓ Dockerfile found")

        dockerfile_structure = check_dockerfile_structure(project_path)

        if dockerfile_structure["valid"]:
            print("✓ Dockerfile structure valid")
        else:
            print("⚠ Dockerfile structure incomplete")

            for instruction in dockerfile_structure["missing"]:
                print("  Missing:", instruction)

    else:
        print("✗ Dockerfile missing")

    if docker_results["Docker Compose"]:
        print("✓ Docker Compose file found")
    else:
        print("⚠ Docker Compose file missing")

    print("\n============================")


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