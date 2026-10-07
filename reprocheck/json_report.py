import json

from reprocheck.repository import (
    check_readme,
    check_license,
    check_dependencies
)

from reprocheck.dependencies import read_dependencies
from reprocheck.import_checker import find_imports
from reprocheck.dependency_checker import check_dependency_mismatches
from reprocheck.file_checker import check_absolute_paths

from reprocheck.docker_checker import (
    check_docker_files,
    check_dockerfile_structure
)


def collect_results(project_path):
    """Collect all ReproCheck results for a project."""

    docker_results = check_docker_files(project_path)
    docker_structure = check_dockerfile_structure(project_path)

    results = {
        "repository": {
            "README": check_readme(project_path),
            "LICENSE": check_license(project_path),
            "Dependencies": check_dependencies(project_path)
        },

        "dependencies": {
            "declared": read_dependencies(project_path),
            "imported": find_imports(project_path),
            "mismatches": check_dependency_mismatches(project_path)
        },

        "paths": {
            "hardcoded_paths": check_absolute_paths(project_path)
        },

        "docker": {
            "Dockerfile": docker_results["Dockerfile"],
            "Docker Compose": docker_results["Docker Compose"],
            "Dockerfile structure valid": docker_structure["valid"],
            "missing instructions": docker_structure["missing"]
        }
    }

    return results


def save_json_report(project_path, results, output_path):
    """Save ReproCheck results as a JSON report."""

    report = {
        "project": str(project_path),
        "results": results
    }

    with open(output_path, "w") as file:
        json.dump(report, file, indent=4)