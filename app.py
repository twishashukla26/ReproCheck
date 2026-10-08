"""PreFlight - Reproducibility Auditor (thin Streamlit interface).

Place this file in the project ROOT (next to the reprocheck/ package and
benchmark_projects/), then run:  streamlit run app.py

This file contains NO audit logic. It only calls the existing backend
function build_check_results(project_path) and displays the CheckResult
objects it returns.
"""
import json
import traceback
from dataclasses import asdict
from pathlib import Path

import streamlit as st

# The one backend import. The folder is still called "reprocheck" on disk.
from reprocheck.main import build_check_results

BENCHMARK_DIR = Path("benchmark_projects")
BENCHMARKS = [
    "project_clean",
    "project_missing_dependency",
    "project_hardcoded_path",
    "project_docker",
]
CUSTOM = "Custom path..."
ICONS = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌"}

st.set_page_config(page_title="PreFlight", page_icon="✈️", layout="centered")

# ---------------------------------------------------------------- header
st.markdown(
    "<h1 style='text-align:center;margin-bottom:0'>PreFlight</h1>"
    "<p style='text-align:center;font-size:1.1rem;margin-top:0'>Reproducibility Auditor</p>"
    "<p style='text-align:center;opacity:.7'>Can another person actually reproduce this?</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- input
choice = st.selectbox("Project", BENCHMARKS + [CUSTOM])
if choice == CUSTOM:
    project_path = Path(st.text_input("Project folder path").strip().strip('"'))
else:
    project_path = BENCHMARK_DIR / choice

_, mid, _ = st.columns([1, 1, 1])
run = mid.button("Run Audit", type="primary", use_container_width=True)

# ---------------------------------------------------------------- run backend
if run:
    st.session_state.pop("audit", None)
    if not project_path.exists() or not project_path.is_dir():
        st.error("Project path not found.")
    else:
        try:
            with st.spinner("Auditing project..."):
                results = build_check_results(str(project_path))
            st.session_state["audit"] = {"project": str(project_path), "results": results}
        except Exception as e:  # shown briefly, full traceback kept for development
            st.error(f"Audit failed: {e}")
            with st.expander("Technical details"):
                st.code(traceback.format_exc())

# ---------------------------------------------------------------- display
audit = st.session_state.get("audit")
if audit:
    results = audit["results"]
    passed = [r for r in results if r.status == "PASS"]
    warnings = [r for r in results if r.status == "WARNING"]
    failed = [r for r in results if r.status == "FAIL"]

    st.divider()
    st.subheader("Audit Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Passed", len(passed))
    c2.metric("Warnings", len(warnings))
    c3.metric("Failed", len(failed))

    st.divider()
    st.subheader("Audit Results")
    st.table(
        [
            {
                "Check": r.name,
                "Status": f"{ICONS.get(r.status, '•')} {r.status}",
                "Message": r.message,
            }
            for r in results
        ]
    )

    # JSON built from the same CheckResult objects the backend returned
    report = {
        "project": audit["project"],
        "summary": {"passed": len(passed), "warnings": len(warnings), "failed": len(failed)},
        "results": [asdict(r) for r in results],
    }
    _, mid, _ = st.columns([1, 2, 1])
    mid.download_button(
        "Download JSON Report",
        data=json.dumps(report, indent=2),
        file_name="preflight_report.json",
        mime="application/json",
        use_container_width=True,
    )
