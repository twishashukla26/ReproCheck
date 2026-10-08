"""PreFlight - Reproducibility Auditor (Streamlit interface).

Run:  streamlit run app.py

The ONLY part you need to edit to connect your backend is `run_backend()`.
Everything else (UI, summary counts, JSON download) works off the normalized
format described in `normalize()`.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

# ----------------------------------------------------------------------------
# 1. BACKEND CONNECTION  (edit this section)
# ----------------------------------------------------------------------------
DEMO_MODE = True  # set to False once run_backend() is connected


def run_backend(project_path: Path) -> dict:
    """Call your existing audit engine on a local folder and return its result.

    Pick ONE of the options below and delete the other.
    """
    # OPTION A - your engine is a Python function:
    #   from preflight.engine import audit_project      # <- your real import
    #   return audit_project(str(project_path))

    # OPTION B - your engine is a CLI that can print JSON:
    #   out = subprocess.run(
    #       [sys.executable, "main.py", str(project_path), "--json"],  # <- your real command
    #       capture_output=True, text=True, check=True,
    #   )
    #   return json.loads(out.stdout)

    raise NotImplementedError("Connect your backend in run_backend().")


def normalize(raw: dict) -> list[dict]:
    """Convert your backend output to: [{"name", "status", "detail"}, ...]
    where status is PASS, WARNING or FAIL. Adjust the key names below
    to match what your backend returns."""
    checks = []
    for item in raw.get("checks", []):
        status = str(item.get("status", "")).upper()
        if status in ("OK", "PASSED"):
            status = "PASS"
        elif status in ("WARN", "WARNINGS"):
            status = "WARNING"
        elif status in ("FAILED", "ERROR"):
            status = "FAIL"
        checks.append(
            {
                "name": item.get("name", "Unknown"),
                "status": status,
                "detail": item.get("message", item.get("detail", "")),
            }
        )
    return checks


DEMO_RESULT = {
    "checks": [
        {"name": "README", "status": "PASS", "message": "README.md found"},
        {"name": "LICENSE", "status": "PASS", "message": "MIT license found"},
        {"name": "Dependencies", "status": "PASS", "message": "requirements.txt found"},
        {"name": "Docker Compose", "status": "WARNING", "message": "No docker-compose.yml"},
        {"name": "Dockerfile", "status": "FAIL", "message": "No Dockerfile found"},
    ]
}


# ----------------------------------------------------------------------------
# 2. URL -> local folder
# ----------------------------------------------------------------------------
def fetch_project(url: str) -> tuple[Path, Path | None]:
    """Return (project_path, temp_dir_to_cleanup). Accepts a Git URL or a local path."""
    local = Path(url).expanduser()
    if local.exists():
        return local, None
    tmp = Path(tempfile.mkdtemp(prefix="preflight_"))
    subprocess.run(
        ["git", "clone", "--depth", "1", url, str(tmp / "repo")],
        check=True, capture_output=True, text=True, timeout=120,
    )
    return tmp / "repo", tmp


def audit(url: str) -> list[dict]:
    if DEMO_MODE:
        return normalize(DEMO_RESULT)
    project, tmp = fetch_project(url)
    try:
        return normalize(run_backend(project))
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------------
# 3. UI
# ----------------------------------------------------------------------------
st.set_page_config(page_title="PreFlight", page_icon="✈️", layout="centered")

st.markdown(
    "<h1 style='text-align:center;margin-bottom:0'>PreFlight</h1>"
    "<p style='text-align:center;font-size:1.1rem;margin-top:0'>Reproducibility Auditor</p>"
    "<p style='text-align:center;opacity:.7'>Can another person actually reproduce this?</p>",
    unsafe_allow_html=True,
)

url = st.text_input("Project URL", placeholder="https://github.com/user/repository")
_, mid, _ = st.columns([1, 1, 1])
run = mid.button("Run Audit", type="primary", use_container_width=True)

if run:
    if not url.strip() and not DEMO_MODE:
        st.warning("Please enter a project URL.")
    else:
        try:
            with st.spinner("Auditing project..."):
                st.session_state["results"] = audit(url.strip())
        except subprocess.CalledProcessError as e:
            st.error(f"Could not fetch the repository.\n\n{e.stderr}")
        except Exception as e:  # noqa: BLE001
            st.error(f"Audit failed: {e}")

results = st.session_state.get("results")
if results:
    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "WARNING", "FAIL")}

    st.divider()
    st.subheader("Audit Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Passed", counts["PASS"])
    c2.metric("Warnings", counts["WARNING"])
    c3.metric("Failed", counts["FAIL"])

    st.divider()
    st.subheader("Audit Results")
    icons = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌"}
    for r in results:
        left, right = st.columns([3, 1])
        left.markdown(f"{icons.get(r['status'], '•')} **{r['name']}**")
        right.markdown(f"`{r['status']}`")
        if r["detail"]:
            left.caption(r["detail"])

    report = {"project": url.strip(), "summary": counts, "results": results}
    _, mid, _ = st.columns([1, 2, 1])
    mid.download_button(
        "Download JSON Report",
        data=json.dumps(report, indent=2),
        file_name="preflight_report.json",
        mime="application/json",
        use_container_width=True,
    )
