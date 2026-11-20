@echo off
title EDM Early-Warning Testbed Launcher
cd /d "%~dp0"
echo =====================================================================
echo  EDUCATIONAL DATA MINING (EDM) EARLY-WARNING TESTBED
echo  Benchmark Dataset: StudyChat (LAK 2026)
echo  Menjalankan server Streamlit pada http://localhost:8501 ...
echo =====================================================================
python app.py
pause
