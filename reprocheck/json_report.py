import json

from reprocheck.repository import (
    check_readme,
    check_license,
    check_dependencies
)

from reprocheck.docker_checker import check_docker_files


def collect_results(project_path):
    """Collect actual ReproCheck results for a project."""

    docker_results = check_docker_files(project_path)

    results = {
        "README": check_readme(project_path),
        "LICENSE": check_license(project_path),
        "Dependencies": check_dependencies(project_path),
        "Dockerfile": docker_results["Dockerfile"],
        "Docker Compose": docker_results["Docker Compose"]
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