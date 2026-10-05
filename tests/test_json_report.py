import json

from reprocheck.json_report import save_json_report


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