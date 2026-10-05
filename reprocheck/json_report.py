import json


def save_json_report(project_path, results, output_path):
    """Save ReproCheck results as a JSON report."""

    report = {
        "project": str(project_path),
        "results": results
    }

    with open(output_path, "w") as file:
        json.dump(report, file, indent=4)