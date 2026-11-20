# -*- coding: utf-8 -*-
"""
core/config.py
Configuration constants, paths, design tokens, and research metadata.
Strictly professional: zero emojis, calibrated academic light indigo design.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "studychat_cohort.json"
FALLBACK_DATA_PATH = BASE_DIR / "vocational_datamining_testbed" / "studychat_web_data.json"

# Project Metadata
PROJECT_TITLE = "EDM Early-Warning Testbed"
PROJECT_SUBTITLE = "Predictive Modeling of Academic At-Risk Students from Chatbot Dialogue Dynamics"
STUDENT_NAME = "Muhammad Rayhan Najib"
STUDENT_NIM = "240533600012"
COURSE_NAME = "Data Mining & Data Science"
INSTITUTION = "University of Massachusetts Amherst (Benchmark StudyChat)"

# Academic Citation
CITATION_APA = (
    "McNichols, H., Ikram, F., & Lan, A. (2026). The StudyChat Dataset: Analyzing Student "
    "Dialogues With ChatGPT in an Artificial Intelligence Course. In Proceedings of the 16th "
    "International Learning Analytics and Knowledge Conference (LAK 2026), pp. 53-63. "
    "ACM. https://doi.org/10.1145/3785022.3785029"
)
CITATION_BIBTEX = """@inproceedings{mcnichols2026studychat,
  title={The StudyChat Dataset: Analyzing Student Dialogues With ChatGPT in an Artificial Intelligence Course},
  author={McNichols, Hunter and Ikram, Fareya and Lan, Andrew},
  booktitle={Proceedings of the 16th International Learning Analytics and Knowledge Conference (LAK 2026)},
  pages={53--63},
  year={2026},
  doi={10.1145/3785022.3785029}
}"""
DATASET_LICENSE = "Creative Commons Attribution 4.0 International (CC BY 4.0)"

# Reproducibility
RANDOM_SEED = 42

# Target Definition
TARGET_COLUMN = "at_risk"
TARGET_THRESHOLD = 0.85  # no_llm_score < 0.85

# UI Color Tokens (Academic Light Indigo System)
COLORS = {
    "primary": "#4338ca",       # Indigo 700 (Structure & branding)
    "primary_light": "#e0e7ff", # Indigo 100
    "accent": "#0284c7",        # Sky 600 (Secondary highlights)
    "accent_light": "#e0f2fe",  # Sky 100
    "at_risk": "#e11d48",       # Rose 600 (Positive/At-Risk class)
    "at_risk_bg": "#ffe4e6",    # Rose 100
    "safe": "#059669",          # Emerald 600 (Negative/Good standing)
    "safe_bg": "#d1fae5",       # Emerald 100
    "neutral_dark": "#0f172a",  # Slate 900 (Headings, primary text)
    "neutral_muted": "#475569", # Slate 600 (Body, captions)
    "neutral_light": "#f8faff", # Base app background
    "card_bg": "#ffffff",       # Card container background
    "border": "#e2e8f0",        # Neutral border line
    "grid": "#f1f5f9",          # Chart grid line
}
