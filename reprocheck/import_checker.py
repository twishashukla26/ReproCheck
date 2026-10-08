import ast
from pathlib import Path


def find_imports(project_path):
    """Find imported libraries from Python files."""

    project = Path(project_path)

    imports = []

    for python_file in project.rglob("*.py"):

        with open(python_file, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for imported in node.names:
                    imports.append(imported.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

    return imports