from pathlib import Path
import re


def check_file_exists(project_path, file_path):
    """Check whether a referenced file exists in the project."""

    project = Path(project_path)
    target_file = project / file_path

    return target_file.exists()


def check_absolute_paths(project_path):
    """Find hard-coded absolute paths in Python files."""

    project = Path(project_path)
    absolute_paths = []

    windows_pattern = re.compile(r"[A-Za-z]:\\")
    unix_pattern = re.compile(r"['\"]/(?:home|Users|mnt|var|tmp|opt|etc)/")

    for python_file in project.rglob("*.py"):

        with open(python_file, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if windows_pattern.search(line) or unix_pattern.search(line):

                    absolute_paths.append(
                        (
                            str(python_file),
                            line_number,
                            line.strip()
                        )
                    )

    return absolute_paths