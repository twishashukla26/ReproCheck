import json

from reprocheck.json_report import (
    collect_results,
    save_json_report
)


def test_collect_results():

    project = "benchmark_projects/project_docker"

    results = collect_results(project)

    assert results["README"] is False
    assert results["LICENSE"] is False
    assert results["Dependencies"] is True
    assert results["Dockerfile"] is True
    assert results["Docker Compose"] is True


def test_save_json_report(tmp_path):

    output_file = tmp_path / "report.json"

    results = {
        "README": True,
        "LICENSE": True,
        "Dockerfile": False
    }

    save_json_report(
        "benchmark_projects/project_clean",
        results,
        output_file
    )

    with open(output_file, "r") as file:
        report = json.load(file)

    assert report["project"] == "benchmark_projects/project_clean"
    assert report["results"]["README"] is True
    assert report["results"]["LICENSE"] is True
    assert report["results"]["Dockerfile"] is False