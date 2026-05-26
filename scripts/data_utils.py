"""
Shared data loading and preprocessing utilities across all analysis scripts.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
TEMPLATES_DIR = DATA_DIR / "templates"

TEAM_ALIASES = {
    "red_bull": "Red Bull Racing",
    "mercedes": "Mercedes-AMG Petronas",
    "ferrari": "Ferrari",
    "mclaren": "McLaren Racing",
    "alpine": "Alpine F1 Team",
    "aston_martin": "Aston Martin F1",
    "alphatauri": "AlphaTauri / RB",
    "rb": "AlphaTauri / RB",
    "alfa": "Alfa Romeo / Sauber",
    "sauber": "Alfa Romeo / Sauber",
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


def build_team_performance_profile() -> pd.DataFrame:
    """
    Merges constructor standings with valuation data to create
    a combined performance + commercial profile per team per year.
    """
    standings = load_constructor_standings()
    valuations = load_team_valuations()

    standings["team_normalized"] = standings["constructor_name"].str.lower().str.replace(r"[^a-z]", "", regex=True)
    valuations["team_normalized"] = valuations["team"].str.lower().str.replace(r"[^a-z]", "", regex=True)

    merged = pd.merge(standings, valuations, on=["year", "team_normalized"], how="left")
    return merged


def compute_commercial_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a normalized commercial index combining valuation,
    social following, and sponsorship value.
    Useful for ranking teams by commercial weight.
    """
    social = load_social_media()
    social = social[social["team"] != "Formula 1 (official)"]
    social["team_normalized"] = social["team"].str.lower().str.replace(r"[^a-z]", "", regex=True)

    df = df.copy()
    if "team_normalized" not in df.columns:
        df["team_normalized"] = df["constructor_name"].str.lower().str.replace(r"[^a-z]", "", regex=True)

    df = pd.merge(df, social[["year", "team_normalized", "instagram_followers_m"]], on=["year", "team_normalized"], how="left")

    if "valuation_usd_m" in df.columns and "instagram_followers_m" in df.columns:
        from sklearn.preprocessing import MinMaxScaler  # optional dependency
        scaler = MinMaxScaler()
        cols = ["valuation_usd_m", "instagram_followers_m"]
        available = [c for c in cols if c in df.columns and df[c].notna().any()]
        if available:
            df["commercial_index"] = scaler.fit_transform(df[available].fillna(0)).mean(axis=1)
    return df
