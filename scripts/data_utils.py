"""
Shared data loading and preprocessing utilities across all analysis scripts.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
TEMPLATES_DIR = DATA_DIR / "templates"

# NOTE: canonical team name mappings for the analysis pipeline live in analyze.py (team_map).
# This alias dict is kept for reference only and is not used in the main pipeline.
TEAM_ALIASES = {
    "red_bull": "Red Bull Racing",
    "mercedes": "Mercedes-AMG Petronas",
    "ferrari": "Ferrari",
    "mclaren": "McLaren Racing",
    "alpine": "Alpine F1 Team",
    "aston_martin": "Aston Martin F1",
    "alphatauri": "AlphaTauri / RB",   # 2023 name
    "racing_bulls": "Racing Bulls",     # 2024-2025 rebrand
    "alfa": "Alfa Romeo / Sauber",      # 2023 name
    "kick_sauber": "Kick Sauber",       # 2024-2025 name
    "haas": "Haas F1 Team",
    "williams": "Williams Racing",
}

TEAM_COLORS = {
    "Red Bull Racing": "#1E41FF",
    "Mercedes-AMG Petronas": "#00D2BE",
    "Ferrari": "#DC0000",
    "McLaren Racing": "#FF8700",
    "Alpine F1 Team": "#0090FF",
    "Aston Martin F1": "#006F62",
    "AlphaTauri / RB": "#2B4562",
    "Alfa Romeo / Sauber": "#900000",
    "Haas F1 Team": "#B6BABD",
    "Williams Racing": "#005AFF",
}


def load_constructor_standings() -> pd.DataFrame:
    path = RAW_DIR / "standings" / "constructor_standings.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run collect_f1_standings.py first: {path}")
    return pd.read_csv(path)


def load_driver_standings() -> pd.DataFrame:
    path = RAW_DIR / "standings" / "driver_standings.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run collect_f1_standings.py first: {path}")
    return pd.read_csv(path)


def load_race_results() -> pd.DataFrame:
    path = RAW_DIR / "standings" / "race_results.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run collect_f1_standings.py first: {path}")
    return pd.read_csv(path)


def load_viewership() -> pd.DataFrame:
    return pd.read_csv(TEMPLATES_DIR / "viewership.csv")


def load_team_valuations() -> pd.DataFrame:
    return pd.read_csv(TEMPLATES_DIR / "team_valuations.csv")


def load_sponsorship() -> pd.DataFrame:
    return pd.read_csv(TEMPLATES_DIR / "sponsorship_values.csv")


def load_attendance() -> pd.DataFrame:
    return pd.read_csv(TEMPLATES_DIR / "attendance.csv")


def load_social_media() -> pd.DataFrame:
    return pd.read_csv(TEMPLATES_DIR / "social_media.csv")


# NOTE: build_team_performance_profile is not used in the main analysis pipeline.
# It uses a naive name normalization that lacks the full team_map from analyze.py,
# so it would produce incorrect merges for Alpine, Aston Martin, AlphaTauri/RB,
# Alfa Romeo/Sauber, Racing Bulls, Kick Sauber, and Haas. Do not call this function
# without first applying the canonical team_map from analyze.py.


# compute_commercial_index removed: was dead code with an undeclared sklearn dependency.
