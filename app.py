"""PreFlight - Reproducibility Auditor.

Streamlit interface for auditing public GitHub repositories.

Run with:
    streamlit run app.py
"""

import json
import traceback
from dataclasses import asdict

import streamlit as st

from reprocheck.github import clone_repository, cleanup_repository
from reprocheck.main import build_check_results


ICONS = {
    "PASS": "✅",
    "WARNING": "⚠️",
    "FAIL": "❌",
}


st.set_page_config(
    page_title="PreFlight",
    page_icon="✈️",
    layout="centered",
)


# ----------------------------------------------------------------
# Header
# ----------------------------------------------------------------

st.markdown(
    "<h1 style='text-align:center;margin-bottom:0'>PreFlight</h1>"
    "<p style='text-align:center;font-size:1.1rem;margin-top:0'>"
    "Reproducibility Auditor"
    "</p>"
    "<p style='text-align:center;opacity:.7'>"
    "Can another person actually reproduce this?"
    "</p>",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------
# GitHub input
# ----------------------------------------------------------------

st.subheader("GitHub Repository")

repo_url = st.text_input(
    "Enter a public GitHub repository URL",
    placeholder="https://github.com/username/repository",
)


# ----------------------------------------------------------------
# Run audit
# ----------------------------------------------------------------

_, mid, _ = st.columns([1, 1, 1])

run = mid.button(
    "Run Audit",
    type="primary",
    use_container_width=True,
)


# ----------------------------------------------------------------
# Run backend
# ----------------------------------------------------------------

if run:

    st.session_state.pop("audit", None)

    if not repo_url.strip():
        st.error("Please enter a GitHub repository URL.")

    else:

        repository_path = None

        try:

            with st.spinner("Cloning repository..."):

                repository_path = clone_repository(repo_url.strip())

            with st.spinner("Auditing repository..."):

                results = build_check_results(
                    str(repository_path)
                )

            st.session_state["audit"] = {
                "project": repo_url.strip(),
                "results": results,
            }

            st.success("Audit completed successfully.")

        except Exception as e:

            st.error(f"Audit failed: {e}")

            with st.expander("Technical details"):
                st.code(traceback.format_exc())

        finally:

            if repository_path is not None:
                cleanup_repository(repository_path)


# ----------------------------------------------------------------
# Display results
# ----------------------------------------------------------------

audit = st.session_state.get("audit")


if audit:

    results = audit["results"]

    passed = [
        r for r in results
        if r.status == "PASS"
    ]

    warnings = [
        r for r in results
        if r.status == "WARNING"
    ]

    failed = [
        r for r in results
        if r.status == "FAIL"
    ]


    st.divider()

    st.subheader("Audit Summary")


    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Passed",
        len(passed),
    )

    c2.metric(
        "Warnings",
        len(warnings),
    )

    c3.metric(
        "Failed",
        len(failed),
    )


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


    # ------------------------------------------------------------
    # JSON report
    # ------------------------------------------------------------

    report = {
        "project": audit["project"],
        "summary": {
            "passed": len(passed),
            "warnings": len(warnings),
            "failed": len(failed),
        },
        "results": [
            asdict(r)
            for r in results
        ],
    }


    st.divider()

    _, mid, _ = st.columns([1, 2, 1])

    mid.download_button(
        "Download JSON Report",
        data=json.dumps(
            report,
            indent=2,
        ),
        file_name="preflight_report.json",
        mime="application/json",
        use_container_width=True,
    )
