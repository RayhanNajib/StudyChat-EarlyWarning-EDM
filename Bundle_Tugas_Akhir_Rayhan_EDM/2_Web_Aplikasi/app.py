# -*- coding: utf-8 -*-
"""
app.py
Single Main Entry Point for Educational Data Mining Early-Warning Testbed.

How to run:
    python app.py
    -> Automatically launches Streamlit on port 8501, opens the browser,
       and navigates to http://localhost:8501 smoothly.
"""
from __future__ import annotations
import os
import sys
import time
import threading
import webbrowser
import subprocess

# ---------------------------------------------------------------------------
# Streamlit Runtime Detection
# ---------------------------------------------------------------------------
def _is_running_in_streamlit() -> bool:
    """Returns True if the script is running inside an active Streamlit server context."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return False


def _launch_streamlit_server() -> None:
    """Spawns Streamlit subprocess and automatically opens browser at http://localhost:8501."""
    script_path = os.path.abspath(__file__)
    port = 8501
    url = f"http://localhost:{port}"

    print("=" * 70)
    print(" EDUCATIONAL DATA MINING (EDM) EARLY-WARNING TESTBED")
    print(" Benchmark Dataset: StudyChat (LAK 2026, arXiv:2503.07928)")
    print("=" * 70)
    print(f"[*] Menyiapkan server Streamlit pada {url}...")
    print("[*] Peramban (browser) akan terbuka secara otomatis dalam beberapa detik.")
    print("[*] Tekan Ctrl+C di terminal ini untuk menghentikan server.\n")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        script_path,
        "--server.port",
        str(port),
        "--server.headless",
        "false",
        "--browser.gatherUsageStats",
        "false",
    ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n[*] Server Streamlit dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\n[!] Gagal menjalankan server Streamlit: {e}")


# ---------------------------------------------------------------------------
# Streamlit Web Application Interface
# ---------------------------------------------------------------------------
def main():
    import streamlit as st
    from core.config import PROJECT_TITLE, STUDENT_NAME, STUDENT_NIM
    from core.ui import apply_custom_css

    st.set_page_config(
        page_title="EDM Early-Warning Testbed",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_custom_css()

    # Sidebar Header branding
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 12px 0 16px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 14px;">
                <div style="font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: #4338ca; font-weight: 700;">
                    Data Mining & Data Science
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-top: 2px;">
                    EDM Early-Warning Testbed
                </div>
                <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">
                    {STUDENT_NAME} — {STUDENT_NIM}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Multi-page navigation using Streamlit native st.navigation
    pages = [
        st.Page("views/1_overview.py", title="Executive Overview"),
        st.Page("views/2_exploration.py", title="Dinamika Dialog & Gap"),
        st.Page("views/3_preparation.py", title="Preparasi & Zero Leakage"),
        st.Page("views/4_modelling.py", title="Arena Model & Leaderboard"),
        st.Page("views/5_evaluation.py", title="Diagnostik & Eksplanabilitas"),
        st.Page("views/6_prediction.py", title="Simulasi Inferensi Risiko"),
        st.Page("views/7_recommendations.py", title="Panduan Intervensi Dosen"),
    ]

    nav = st.navigation(pages)
    nav.run()

    # Sidebar Footer
    with st.sidebar:
        st.markdown(
            """
            <div style="padding-top: 20px; font-size: 0.72rem; color: #94a3b8; border-top: 1px solid #e2e8f0; margin-top: 30px;">
                StudyChat Benchmark • LAK 2026<br>
                Host: http://localhost:8501
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    if _is_running_in_streamlit():
        main()
    else:
        _launch_streamlit_server()
