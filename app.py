"""PreFlight - Reproducibility Auditor (thin Streamlit UI).

Run with:  python -m streamlit run app.py

This file only handles the interface. All audit logic stays in the
existing `reprocheck` package (clone, audit, cleanup).
"""
import io
import json
import re
import traceback
from dataclasses import asdict, is_dataclass
from datetime import date
from xml.sax.saxutils import escape

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer

from reprocheck.github import cleanup_repository, clone_repository
from reprocheck.main import build_check_results

ICONS = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌"}
PDF_COLORS = {"PASS": "#2e7d32", "WARNING": "#ef6c00", "FAIL": "#c62828"}

# Public GitHub repo only: https://github.com/<owner>/<repo>[.git][/]
GITHUB_URL = re.compile(
    r"^https://(www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?(\.git)?/?$"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def result_to_dict(result) -> dict:
    """Turn one CheckResult object into a plain dict (name, status, message)."""
    data = asdict(result) if is_dataclass(result) else {
        "name": result.name,
        "status": result.status,
        "message": result.message,
    }
    status = data["status"]
    status = getattr(status, "value", status)  # works if status is an Enum
    data["status"] = str(status).upper()
    return {
        "name": str(data["name"]),
        "status": data["status"],
        "message": str(data["message"]),
    }


def build_report(url: str, results: list) -> dict:
    rows = [result_to_dict(r) for r in results]
    return {
        "project": url,
        "summary": {
            "passed": sum(r["status"] == "PASS" for r in rows),
            "warnings": sum(r["status"] == "WARNING" for r in rows),
            "failed": sum(r["status"] == "FAIL" for r in rows),
        },
        "results": rows,
    }


def build_pdf(report: dict) -> bytes:
    """Simple A4 PDF made from the same report dict shown in the UI."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, title="PreFlight Report",
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    check_style = ParagraphStyle("check", parent=styles["Normal"], fontName="Helvetica-Bold")

    summary = report["summary"]
    story = [
        Paragraph("PreFlight", styles["Title"]),
        Paragraph("Reproducibility Audit Report", styles["Heading2"]),
        Spacer(1, 0.4 * cm),
        Paragraph(f"<b>Repository:</b> {escape(report['project'])}", styles["Normal"]),
        Paragraph(f"<b>Date:</b> {date.today().isoformat()}", styles["Normal"]),
        Spacer(1, 0.6 * cm),
        Paragraph("Audit Summary", styles["Heading2"]),
        Paragraph(f"Passed: {summary['passed']}", styles["Normal"]),
        Paragraph(f"Warnings: {summary['warnings']}", styles["Normal"]),
        Paragraph(f"Failed: {summary['failed']}", styles["Normal"]),
        Spacer(1, 0.6 * cm),
        Paragraph("Audit Results", styles["Heading2"]),
    ]

    for r in report["results"]:
        color = PDF_COLORS.get(r["status"], "#000000")
        story.append(
            KeepTogether([
                Paragraph(escape(r["name"]), check_style),
                Paragraph(f'<font color="{color}"><b>{escape(r["status"])}</b></font>', styles["Normal"]),
                Paragraph(escape(r["message"]), styles["Normal"]),
                Spacer(1, 0.35 * cm),
            ])
        )

    doc.build(story)
    return buffer.getvalue()


def run_audit(url: str) -> None:
    """Clone -> audit -> always clean up. Stores output in session state."""
    repo_path = None
    try:
        try:
            with st.spinner("Cloning repository..."):
                repo_path = clone_repository(url)
        except Exception as exc:  # noqa: BLE001
            st.error("Could not clone the repository.")
            st.write(
                "Check that the URL is correct and the repository is public. "
                f"({type(exc).__name__}: {str(exc)[:200]})"
            )
            with st.expander("Technical details"):
                st.code(traceback.format_exc())
            return

        try:
            with st.spinner("Auditing repository..."):
                results = build_check_results(str(repo_path))
            report = build_report(url, results)
            st.session_state["report"] = report
            st.session_state["json_bytes"] = json.dumps(report, indent=2).encode("utf-8")
            st.session_state["pdf_bytes"] = build_pdf(report)
        except Exception as exc:  # noqa: BLE001
            st.error("Audit failed.")
            st.write(f"{type(exc).__name__}: {str(exc)[:200]}")
            with st.expander("Technical details"):
                st.code(traceback.format_exc())
    finally:
        if repo_path is not None:
            try:
                cleanup_repository(repo_path)
            except Exception as exc:  # noqa: BLE001
                st.warning(f"Could not delete the temporary repository: {exc}")


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="PreFlight", page_icon="✈️", layout="centered")

st.markdown(
    "<h1 style='text-align:center;margin-bottom:0'>PreFlight</h1>"
    "<h3 style='text-align:center;margin-top:0;font-weight:400'>Reproducibility Auditor</h3>"
    "<p style='text-align:center;opacity:.7'>Can another person actually reproduce this?</p>",
    unsafe_allow_html=True,
)

repo_url = st.text_input(
    "GitHub Repository", placeholder="https://github.com/username/repository"
)
_, center, _ = st.columns([1, 1, 1])
run_clicked = center.button("Run Audit", type="primary", use_container_width=True)

if run_clicked:
    url = repo_url.strip()
    if not url:
        st.error("Please enter a GitHub repository URL.")
    elif not GITHUB_URL.match(url):
        st.error(
            "That doesn't look like a GitHub repository URL. "
            "Use the format https://github.com/username/repository"
        )
    else:
        st.session_state.pop("report", None)  # clear the previous audit
        run_audit(url)

report = st.session_state.get("report")
if report:
    st.divider()
    st.subheader("Audit Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Passed", report["summary"]["passed"])
    c2.metric("Warnings", report["summary"]["warnings"])
    c3.metric("Failed", report["summary"]["failed"])

    st.divider()
    st.subheader("Audit Results")
    st.dataframe(
        [
            {
                "Check": r["name"],
                "Status": f"{ICONS.get(r['status'], '')} {r['status']}",
                "Message": r["message"],
            }
            for r in report["results"]
        ],
        hide_index=True,
    )

    st.divider()
    d1, d2 = st.columns(2)
    d1.download_button(
        "Download JSON Report",
        data=st.session_state["json_bytes"],
        file_name="preflight_report.json",
        mime="application/json",
        use_container_width=True,
    )
    d2.download_button(
        "Download PDF Report",
        data=st.session_state["pdf_bytes"],
        file_name="preflight_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
