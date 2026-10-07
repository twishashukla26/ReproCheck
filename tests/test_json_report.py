import json

from reprocheck.json_report import (
    collect_results,
    save_json_report
)


def test_collect_results():

    project = "benchmark_projects/project_docker"

    results = collect_results(project)

    assert results["repository"]["README"] is False
    assert results["repository"]["LICENSE"] is False
    assert results["repository"]["Dependencies"] is True

    assert "pandas" in results["dependencies"]["declared"]
    assert "pandas" in results["dependencies"]["imported"]

    assert results["docker"]["Dockerfile"] is True
    assert results["docker"]["Docker Compose"] is True
    assert results["docker"]["Dockerfile structure valid"] is True


def test_save_json_report(tmp_path):

    output_file = tmp_path / "report.json"

    results = {
        "repository": {
            "README": True,
            "LICENSE": True
        },
        "dependencies": {
            "declared": ["pandas"],
            "imported": ["pandas"],
            "mismatches": []
        },
        "paths": {
            "hardcoded_paths": []
        },
        "docker": {
            "Dockerfile": False,
            "Docker Compose": False,
            "Dockerfile structure valid": False,
            "missing instructions": []
        }
    }

    save_json_report(
        "benchmark_projects/project_clean",
        results,
        output_file
    )

    with open(output_file, "r") as file:
        report = json.load(file)

    assert report["project"] == "benchmark_projects/project_clean"
    assert report["results"]["repository"]["README"] is True
    assert report["results"]["repository"]["LICENSE"] is True
    assert report["results"]["dependencies"]["declared"] == ["pandas"]