from reprocheck.repository import (
    check_readme,
    check_license,
    check_dependencies
)

from reprocheck.dependencies import read_dependencies
from reprocheck.import_checker import find_imports

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


    print("\n============================")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide project path")
        exit()

    generate_report(sys.argv[1])