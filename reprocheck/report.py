from .result import CheckResult


def format_report(project, results):
    passed = [r for r in results if r.is_passed()]
    warnings = [r for r in results if r.is_warning()]
    failed = [r for r in results if r.is_failed()]

    lines = []

    lines.append("=" * 40)
    lines.append("        REPROCHECK REPORT")
    lines.append("=" * 40)
    lines.append("")
    lines.append(f"Project: {project}")
    lines.append("")

    lines.append("PASSED")
    lines.append("------")

    if passed:
        for result in passed:
            lines.append(f"  ✓ {result.name}: {result.message}")
    else:
        lines.append("  None")

    lines.append("")
    lines.append("WARNINGS")
    lines.append("--------")

    if warnings:
        for result in warnings:
            lines.append(f"  ⚠ {result.name}: {result.message}")
    else:
        lines.append("  None")

    lines.append("")
    lines.append("FAILED")
    lines.append("------")

    if failed:
        for result in failed:
            lines.append(f"  ✗ {result.name}: {result.message}")
    else:
        lines.append("  None")

    lines.append("")
    lines.append("-" * 40)
    lines.append("Summary")
    lines.append("-------")
    lines.append(f"Passed:   {len(passed)}")
    lines.append(f"Warnings: {len(warnings)}")
    lines.append(f"Failed:   {len(failed)}")
    lines.append("-" * 40)

    return "\n".join(lines)