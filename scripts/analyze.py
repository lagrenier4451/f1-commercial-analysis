"""
Core analysis functions: growth story, team commercial value,
sponsorship ROI, and scenario modeling.

Run: python scripts/analyze.py
Outputs to: data/processed/
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import numpy as np
from data_utils import (
    load_constructor_standings,
    load_viewership,
    load_team_valuations,
    load_sponsorship,
    load_attendance,
    load_social_media,
    TEAM_COLORS,
)

PROCESSED_DIR = Path("data/processed")


# ---------------------------------------------------------------------------
# 1. F1 Growth Story
# ---------------------------------------------------------------------------

def analyze_viewership_growth() -> pd.DataFrame:
    df = load_viewership()
    df["us_viewers_yoy_change_k"] = df["us_avg_per_race_k"].diff()
    # Unique-viewer series only available 2018-2021; use where present
    if df["fom_unique_viewers_m"].notna().any():
        base = df.loc[df["fom_unique_viewers_m"].notna(), "fom_unique_viewers_m"].iloc[0]
        df["unique_viewers_growth_pct_from_2018"] = (
            (df["fom_unique_viewers_m"] / base - 1) * 100
        )
    df.to_csv(PROCESSED_DIR / "viewership_growth.csv", index=False)
    print(f"  Viewership growth analysis saved ({len(df)} rows)")
    return df


def analyze_attendance_trends() -> pd.DataFrame:
    df = load_attendance()
    df = df.sort_values(["country", "year"])
    df["yoy_attendance_change"] = df.groupby("race_name")["attendance_weekend"].diff()
    circuit_summary = (
        df.groupby("race_name")
        .agg(
            country=("country", "first"),
            years_available=("year", "count"),
            avg_attendance=("attendance_weekend", "mean"),
            max_attendance=("attendance_weekend", "max"),
            latest_year=("year", "max"),
        )
        .reset_index()
        .sort_values("avg_attendance", ascending=False)
    )
    circuit_summary.to_csv(PROCESSED_DIR / "attendance_by_circuit.csv", index=False)
    return circuit_summary


# ---------------------------------------------------------------------------
# 2. Team Commercial Value
# ---------------------------------------------------------------------------

def analyze_performance_vs_valuation() -> pd.DataFrame:
    standings = load_constructor_standings()
    valuations = load_team_valuations()

    team_map = {
        # Ferrari
        "ferrari": "Ferrari",
        # Mercedes
        "mercedesamgpetronas": "Mercedes-AMG Petronas",
        "mercedes": "Mercedes-AMG Petronas",
        # Red Bull
        "redbull": "Red Bull Racing",
        "redbullracing": "Red Bull Racing",
        # McLaren
        "mclaren": "McLaren Racing",
        "mclarenracing": "McLaren Racing",
        # Alpine (API uses "alpinefteam", valuation CSV uses "Alpine F1 Team")
        "alpinef1team": "Alpine F1 Team",
        "alpinefteam": "Alpine F1 Team",
        # Aston Martin (API truncates to "astonmartinf", valuation uses "Aston Martin F1")
        "astonmartinf1": "Aston Martin F1",
        "astonmartinf": "Aston Martin F1",
        "astonmartin": "Aston Martin F1",
        # Williams
        "williamsracing": "Williams Racing",
        "williams": "Williams Racing",
        # AlphaTauri / RB (2023 API name "alphatauri", valuation CSV "AlphaTauri / RB")
        "alphatauri": "AlphaTauri / RB",
        "alphataurirb": "AlphaTauri / RB",
        # RB F1 Team (2024 API name "rbfteam", valuation CSV "RB (AlphaTauri)")
        "rbfteam": "RB (AlphaTauri)",
        "rbalphatauri": "RB (AlphaTauri)",
        # Alfa Romeo / Sauber (2023 API name "alfaromeo", valuation CSV "Alfa Romeo / Sauber")
        "alfaromeo": "Alfa Romeo / Sauber",
        "alfaromeosauber": "Alfa Romeo / Sauber",
        # Kick Sauber (2024 API name "sauber", valuation CSV "Kick Sauber")
        "sauber": "Kick Sauber",
        "kicksauber": "Kick Sauber",
        # Haas (API uses "haasfteam")
        "haas": "Haas F1 Team",
        "haasfteam": "Haas F1 Team",
    }
    standings["team_key"] = (
        standings["constructor_name"].str.lower().str.replace(r"[^a-z]", "", regex=True)
    )
    valuations["team_key"] = (
        valuations["team"].str.lower().str.replace(r"[^a-z]", "", regex=True)
    )
    standings["team_canonical"] = standings["team_key"].map(team_map).fillna(standings["constructor_name"])
    valuations["team_canonical"] = valuations["team_key"].map(team_map).fillna(valuations["team"])

    merged = pd.merge(
        standings[["year", "position", "points", "wins", "constructor_name", "team_canonical"]],
        valuations[["year", "team_canonical", "valuation_usd_m", "revenue_usd_m"]],
        on=["year", "team_canonical"],
        how="inner",
    )

    merged["valuation_per_championship_point"] = merged["valuation_usd_m"] / merged["points"].replace(0, np.nan)
    merged["commercial_to_performance_ratio"] = merged["valuation_usd_m"] / (11 - merged["position"])

    merged.to_csv(PROCESSED_DIR / "performance_vs_valuation.csv", index=False)
    print(f"  Performance vs valuation analysis saved ({len(merged)} rows)")
    return merged


def rank_teams_commercial_efficiency() -> pd.DataFrame:
    """
    Which teams get the most commercial value relative to their on-track position?
    A team ranked P5 commercially but P3 on track is 'punching above weight'.
    """
    perf = analyze_performance_vs_valuation()
    social = load_social_media()
    social["team_key"] = social["team"].str.lower().str.replace(r"[^a-z]", "", regex=True)

    summary = (
        perf.groupby("team_canonical")
        .agg(
            avg_championship_position=("position", "mean"),
            avg_valuation_usd_m=("valuation_usd_m", "mean"),
            total_wins=("wins", "sum"),
        )
        .reset_index()
    )

    f1_social = social[social["team"] != "Formula 1 (official)"].sort_values("year", ascending=False)
    f1_social = f1_social.drop_duplicates(subset="team")
    f1_social["team_key"] = f1_social["team"].str.lower().str.replace(r"[^a-z]", "", regex=True)
    summary["team_key"] = summary["team_canonical"].str.lower().str.replace(r"[^a-z]", "", regex=True)

    summary = pd.merge(summary, f1_social[["team_key", "instagram_followers_m"]], on="team_key", how="left")

    summary["commercial_rank"] = summary["avg_valuation_usd_m"].rank(ascending=False)
    summary["performance_rank"] = summary["avg_championship_position"].rank(ascending=True)
    summary["commercial_vs_performance_gap"] = summary["performance_rank"] - summary["commercial_rank"]

    summary = summary.sort_values("avg_valuation_usd_m", ascending=False)
    summary.to_csv(PROCESSED_DIR / "team_commercial_efficiency.csv", index=False)
    return summary


# ---------------------------------------------------------------------------
# 3. Sponsorship ROI
# ---------------------------------------------------------------------------

SPORTS_CPM_BENCHMARKS = {
    "F1 (global)": {"cpm_usd": 28.0, "avg_viewers_per_event_m": 75, "source": "Estimated from FOM data"},
    "NFL (US)": {"cpm_usd": 45.0, "avg_viewers_per_event_m": 17, "source": "Nielsen 2023"},
    "Premier League (UK)": {"cpm_usd": 18.0, "avg_viewers_per_event_m": 1.2, "source": "Various industry reports"},
    "NBA (US)": {"cpm_usd": 25.0, "avg_viewers_per_event_m": 2.1, "source": "Nielsen 2023"},
    "Champions League": {"cpm_usd": 22.0, "avg_viewers_per_event_m": 12, "source": "Industry estimates"},
    "Olympics (summer, global)": {"cpm_usd": 35.0, "avg_viewers_per_event_m": 600, "source": "Various"},
}


def compute_sponsorship_roi_metrics() -> pd.DataFrame:
    viewership = load_viewership()
    sponsorship = load_sponsorship()

    races_per_year = {2018: 21, 2019: 21, 2020: 17, 2021: 22, 2022: 22, 2023: 23, 2024: 24}

    viewership["races"] = viewership["year"].map(races_per_year)
    # Use global_avg_per_race_m where available (2022+); fall back to fom_unique/races for earlier years
    viewership["avg_viewers_per_race_m"] = viewership["global_avg_per_race_m"].fillna(
        viewership["fom_unique_viewers_m"] / viewership["races"]
    )

    avg_viewers = viewership["avg_viewers_per_race_m"].dropna().mean()

    cpm_data = []
    for sport, data in SPORTS_CPM_BENCHMARKS.items():
        cpm_data.append({
            "sport": sport,
            "cpm_usd": data["cpm_usd"],
            "avg_viewers_per_event_m": data["avg_viewers_per_event_m"],
            "cost_per_viewer_usd": data["cpm_usd"] / 1000,
            "source": data["source"],
        })
    cpm_df = pd.DataFrame(cpm_data)
    cpm_df.to_csv(PROCESSED_DIR / "sports_cpm_comparison.csv", index=False)

    team_deals = sponsorship[sponsorship["team_or_entity"] != "Formula 1 (FOM)"].copy()
    team_deals["implied_exposure_per_race_m_viewers"] = avg_viewers * 0.15
    team_deals["implied_cpm"] = (team_deals["annual_value_usd_m"] * 1e6) / (
        team_deals["implied_exposure_per_race_m_viewers"] * 1e6 / 1000
    )

    team_deals.to_csv(PROCESSED_DIR / "sponsorship_roi.csv", index=False)
    print(f"  Sponsorship ROI metrics saved")
    return cpm_df, team_deals


# ---------------------------------------------------------------------------
# 4. Scenario Modeling
# ---------------------------------------------------------------------------

def model_valuation_scenarios(base_year: int = 2023) -> pd.DataFrame:
    """
    Models how team valuations might shift based on championship outcomes.
    Uses historical correlation between position and valuation as a multiplier.
    """
    valuations = load_team_valuations()
    base = valuations[valuations["year"] == base_year].copy()

    perf = analyze_performance_vs_valuation()
    corr_data = perf[["position", "valuation_usd_m"]].dropna()
    if len(corr_data) >= 4:
        from scipy.stats import linregress
        slope, intercept, r, p, _ = linregress(corr_data["position"], corr_data["valuation_usd_m"])
        position_slope = slope
        r_squared = r ** 2
    else:
        position_slope = -150.0
        r_squared = None

    scenarios = []
    for _, row in base.iterrows():
        for scenario_label, position in [("Win WCC (P1)", 1), ("Finish P2", 2), ("Finish P3", 3), ("Midfield (P5)", 5), ("Bottom Half (P8)", 8)]:
            if pd.notna(row["valuation_usd_m"]):
                delta = (position - 5) * position_slope
                adjusted = row["valuation_usd_m"] + delta
                scenarios.append({
                    "team": row["team"],
                    "base_valuation_usd_m": row["valuation_usd_m"],
                    "scenario": scenario_label,
                    "championship_position": position,
                    "modeled_valuation_usd_m": max(adjusted, row["valuation_usd_m"] * 0.5),
                    "valuation_change_usd_m": adjusted - row["valuation_usd_m"],
                    "r_squared": r_squared,
                })

    df = pd.DataFrame(scenarios)
    df.to_csv(PROCESSED_DIR / "valuation_scenarios.csv", index=False)
    r2_str = f"{r_squared:.2f}" if r_squared is not None else "N/A"
    print(f"  Scenario model saved ({len(df)} rows, R²={r2_str})")
    return df


# ---------------------------------------------------------------------------
# Run all analyses
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print("Running analyses...")
    analyze_viewership_growth()
    analyze_attendance_trends()
    analyze_performance_vs_valuation()
    rank_teams_commercial_efficiency()
    compute_sponsorship_roi_metrics()
    model_valuation_scenarios()
    print(f"\nDone. Results in {PROCESSED_DIR}/")
