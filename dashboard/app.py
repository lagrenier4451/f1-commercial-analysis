"""
F1 Commercial Analysis Dashboard
Run: streamlit run dashboard/app.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_utils import TEAM_COLORS

st.set_page_config(
    page_title="F1 Commercial Analysis",
    page_icon="🏎",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROCESSED = Path("data/processed")
TEMPLATES = Path("data/templates")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@st.cache_data
def load(filename: str, base: Path = PROCESSED) -> pd.DataFrame | None:
    path = base / filename
    if not path.exists():
        return None
    return pd.read_csv(path)


def missing_data_warning(name: str):
    st.warning(f"**{name}** not found. Run `python scripts/collect_f1_standings.py` then `python scripts/analyze.py` to generate it.", icon="⚠️")


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/320px-F1.svg.png", width=120)
st.sidebar.title("F1 Commercial Analysis")
st.sidebar.caption("2014 – 2025 | Decline, Acquisition & Resurgence")

section = st.sidebar.radio(
    "Section",
    ["Overview", "F1's Growth Story", "Team Commercial Value", "Sponsorship ROI", "Scenario Modeler"],
    index=0,
)

st.sidebar.divider()
st.sidebar.caption("Data sources: FOM, Sportico, SportsPro, Jolpica API")
st.sidebar.caption("⚠️ Sponsorship values are estimates from public reports unless noted.")

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

if section == "Overview":
    st.title("The Business of Speed")
    st.subheader("A Data-Driven Analysis of F1's Commercial Value (2014–2025)")
    st.markdown("""
    Formula 1 is no longer just a motorsport — it's a global media and marketing property.
    In 2017, Liberty Media acquired F1 from Bernie Ecclestone. What followed is one of sport's
    most dramatic commercial turnarounds: from 352M viewers at the trough (2017) to 6.7M race-day
    attendees in 2025, billion-dollar team valuations, and the most valuable sponsorship roster in motorsport history.

    This analysis covers the full arc — the decline, the acquisition, and the resurgence — through to the record-breaking 2025 season.

    | Pillar | Question |
    |--------|----------|
    | 📈 **Growth Story** | How much did F1's audience and attendance grow — and where did it bottom out? |
    | 🏆 **Team Commercial Value** | Which teams win off-track, and does performance drive valuation? |
    | 💰 **Sponsorship ROI** | Is F1 a good buy for marketers vs. other major sports? |
    """)

    viewership = load("viewership_growth.csv")
    if viewership is not None:
        col1, col2, col3, col4 = st.columns(4)
        peak = viewership["fom_unique_viewers_m"].dropna().max()
        col1.metric("Viewership (unique viewer era)", f"352M trough → {peak:.0f}M peak", "2017 trough to 2018 peak; FOM changed methodology after 2021")
        col2.metric("Races Per Season (2025)", "24", "+5 vs 2014")

        sponsorship = load("sponsorship_roi.csv")
        if sponsorship is not None:
            max_deal = sponsorship["annual_value_usd_m"].max()
            col3.metric("Largest Team Deal (est.)", f"${max_deal:.0f}M/yr", "Oracle × Red Bull Racing 2022")

        valuation = load("performance_vs_valuation.csv")
        if valuation is not None:
            max_val = valuation["valuation_usd_m"].max()
            col4.metric("Highest Team Valuation", f"${max_val/1000:.1f}B", "Ferrari (Sportico Nov 2025)")

        st.divider()
        fig = px.area(
            viewership.dropna(subset=["fom_unique_viewers_m"]),
            x="year", y="fom_unique_viewers_m",
            title="Global Unique TV Viewers (M) — 2014–2021 | The Decline, Trough & Recovery",
            labels={"fom_unique_viewers_m": "Viewers (M)", "year": "Season"},
            color_discrete_sequence=["#E8002D"],
        )
        fig.add_vline(x=2017, line_dash="dash", line_color="gray", annotation_text="Liberty Media acquisition", annotation_position="top right")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Chart shows 2014–2021 only. From 2022, FOM switched to cumulative reporting (total views across all races) — a different methodology not directly comparable to the unique-viewer series above. See F1's Growth Story → Viewership for full context.")
    else:
        missing_data_warning("Viewership growth data")

# ---------------------------------------------------------------------------
# F1's Growth Story
# ---------------------------------------------------------------------------

elif section == "F1's Growth Story":
    st.title("F1's Growth Story")
    st.caption("How Drive to Survive, new markets, and Liberty Media transformed the sport commercially.")

    tab1, tab2, tab3 = st.tabs(["Viewership", "Race Attendance", "Social Media"])

    with tab1:
        viewership = load("viewership_growth.csv")
        if viewership is not None:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    viewership.dropna(subset=["fom_unique_viewers_m"]),
                    x="year", y="fom_unique_viewers_m",
                    title="Global Unique TV Viewers per Season",
                    labels={"fom_unique_viewers_m": "Viewers (M)", "year": "Season"},
                    color="fom_unique_viewers_m",
                    color_continuous_scale="Reds",
                )
                fig.update_layout(showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(
                    viewership.dropna(subset=["us_avg_per_race_k"]),
                    x="year", y="us_avg_per_race_k",
                    title="US Average Viewers Per Race (Thousands)",
                    labels={"us_avg_per_race_k": "Avg Viewers (K)", "year": "Season"},
                    color="us_avg_per_race_k",
                    color_continuous_scale="Blues",
                )
                fig.update_layout(showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Key inflection points:**")
            st.markdown("""
            - **2014–2017**: F1 sheds 73M viewers (-17%) as pay-TV migration restricts free-to-air access across Europe.
            - **2017**: Liberty Media acquisition — 352M viewers, the commercial trough.
            - **2018**: First full Liberty year. Viewer count jumps to 490M (+39% YoY) as distribution deals improve.
            - **2019**: Drive to Survive S1 on Netflix (March). US average +25% YoY (539K → 672K) via new ABC simulcast deal.
            - **2020**: COVID-shortened 17-race calendar (17 races). US average dips to 608K (-10% YoY) as no fan attendance suppressed broadcast interest; global unique viewers fall to 433M.
            - **2021**: Verstappen/Hamilton title fight + DtS S3 & S4. US average jumps to 948K (+56% YoY) — largest single-year US gain on record.
            - **2022**: Miami GP debuts. FOM reports 1.54B cumulative views; 70M per-race average globally.
            - **2023**: Las Vegas GP launches. FOM states record cumulative audiences but withholds exact figure.
            - **2024**: 6.5M total season attendance confirmed by FOM. Miami peaks at 3.1M US viewers.
            - **2025**: Record season. 1.83B cumulative views (+6.8% YoY), 76.1M per-race average. US hits record 1.32M/race. 6.7M total attendance, 19/24 events sold out. Global fanbase reaches 827M.
            """)
        else:
            missing_data_warning("Viewership growth")

    with tab2:
        attendance = load("attendance_by_circuit.csv")
        raw_att = load("attendance.csv", base=Path("data/templates"))
        if raw_att is not None:
            fig = px.bar(
                raw_att.dropna(subset=["attendance_weekend"]).sort_values("attendance_weekend", ascending=False),
                x="race_name", y="attendance_weekend",
                color="country",
                title="Race Weekend Attendance by Event (3-Day Total) — some events share a circuit across years",
                labels={"attendance_weekend": "Attendance", "race_name": "Race"},
            )
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            usa_races = raw_att[raw_att["country"] == "USA"].dropna(subset=["attendance_weekend"])
            if not usa_races.empty:
                fig2 = px.line(
                    usa_races, x="year", y="attendance_weekend", color="race_name",
                    title="US Race Attendance Over Time — The American Expansion",
                    markers=True,
                    labels={"attendance_weekend": "Attendance", "year": "Year", "race_name": "Race"},
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            missing_data_warning("Attendance data")

    with tab3:
        social = load("social_media.csv", base=Path("data/templates"))
        if social is not None:
            team_social = social[social["team"] != "Formula 1 (official)"].copy()
            f1_official = social[social["team"] == "Formula 1 (official)"].copy()

            fig = px.bar(
                team_social.sort_values("instagram_followers_m", ascending=True),
                x="instagram_followers_m", y="team",
                orientation="h",
                title="Instagram Followers by Team — 2023 Blinkfire Data (most recent per-team breakdown available)",
                labels={"instagram_followers_m": "Followers (M)", "team": ""},
                color="team",
                color_discrete_map=TEAM_COLORS,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            if not f1_official.empty:
                col1, col2 = st.columns(2)
                # Use most recent row that actually has instagram data
                ig_row = f1_official.dropna(subset=["instagram_followers_m"]).sort_values("year").iloc[-1] if f1_official["instagram_followers_m"].notna().any() else None
                yt_row = f1_official.dropna(subset=["youtube_subscribers_m"]).sort_values("year").iloc[-1] if f1_official["youtube_subscribers_m"].notna().any() else None
                if ig_row is not None:
                    col1.metric(f"F1 Official Instagram ({int(ig_row['year'])})", f"{ig_row['instagram_followers_m']:.1f}M", "vs 5.6M in 2018")
                else:
                    col1.metric("F1 Official Instagram", "N/A")
                if yt_row is not None:
                    col2.metric(f"F1 Official YouTube ({int(yt_row['year'])})", f"{yt_row['youtube_subscribers_m']:.1f}M")
                else:
                    col2.metric("F1 Official YouTube", "See notes", "Combined platforms: 96M (2024)")
        else:
            missing_data_warning("Social media data")

# ---------------------------------------------------------------------------
# Team Commercial Value
# ---------------------------------------------------------------------------

elif section == "Team Commercial Value":
    st.title("Team Commercial Value")
    st.caption("Does performance drive valuation — or does brand heritage?")

    tab1, tab2 = st.tabs(["Valuation vs Performance", "Commercial Efficiency"])

    with tab1:
        perf = load("performance_vs_valuation.csv")
        if perf is not None:
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.scatter(
                    perf.dropna(subset=["valuation_usd_m"]),
                    x="position", y="valuation_usd_m",
                    color="constructor_name",
                    size="points",
                    hover_data=["year", "wins"],
                    title="Championship Position vs Team Valuation (USD M)",
                    labels={"position": "WCC Position", "valuation_usd_m": "Valuation (USD M)", "constructor_name": "Team"},
                    trendline="ols",
                )
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown("**Reading this chart**")
                st.markdown("""
                Each point is a team-season. Size = championship points earned.

                The trendline shows the correlation between finishing position and estimated valuation.
                A downward slope means **higher-placed teams command higher valuations** — but Ferrari's
                brand power means they sit above the line regardless of position.

                **What to watch for:**
                - Teams that sit above the trendline → commercially overperforming
                - Teams below the trendline → commercially underperforming their results
                """)

            year_options = sorted(perf["year"].unique(), reverse=True)
            selected_year = st.selectbox("Filter by season", ["All"] + [str(y) for y in year_options])
            display = perf if selected_year == "All" else perf[perf["year"] == int(selected_year)]
            table = (
                display[["year", "constructor_name", "position", "points", "wins", "valuation_usd_m"]]
                .dropna(subset=["valuation_usd_m"])
                .sort_values(["year", "position"])
                .rename(columns={
                    "constructor_name": "Team",
                    "position": "WCC Pos",
                    "points": "Points",
                    "wins": "Wins",
                    "valuation_usd_m": "Valuation ($M)",
                })
            )
            table["Valuation ($M)"] = table["Valuation ($M)"].apply(
                lambda x: f"${x:,.0f}" if pd.notna(x) else "—"
            )
            st.caption("Revenue figures are not publicly available from Sportico; valuation uses revenue-multiple methodology.")
            st.dataframe(table, use_container_width=True, hide_index=True)
        else:
            missing_data_warning("Performance vs valuation data")

    with tab2:
        with st.expander("📐 How the Commercial Efficiency Gap is calculated", expanded=False):
            st.markdown("""
            ### Methodology

            The **Commercial vs Performance Gap** measures whether a team's commercial standing
            (valuation) is ahead of or behind its on-track results.

            **Step 1 — Rank each team by valuation**
            Teams are ranked by average Sportico valuation across all available years (2023–2025).
            Teams that changed name mid-period (e.g. AlphaTauri → Racing Bulls, Alfa Romeo → Kick Sauber)
            are treated as separate entities, so the ranking covers 12 entities not 10.
            Rank 1 = highest valued team.

            **Step 2 — Rank each team by championship position**
            Teams are ranked by average WCC finishing position across the same years.
            Rank 1 = best average result (lowest finishing position number).

            **Step 3 — Calculate the gap**
            ```
            Gap = Performance Rank − Commercial Rank
            ```
            - **Positive gap**: The team's commercial rank is *better* (lower number) than its performance rank. The team is valued more highly than its on-track results alone would justify. Example: Ferrari finishes ~P3–4 but is ranked #1 commercially — brand heritage drives valuation beyond results.
            - **Negative gap**: The team's on-track performance rank is *better* than its commercial rank. The team performs above its commercial standing — results not yet fully reflected in valuation. Example: a team that consistently finishes P2 but is ranked only 5th commercially is undervalued relative to results.
            - **Zero / near-zero**: Commercial and performance standing are roughly in line.

            **Important caveat**: The gap is an average across years. A team that recently
            improved (e.g. McLaren 2024–2025) will see their commercial rank catch up to their
            performance rank with a lag, as valuations are published annually.
            """)

        efficiency = load("team_commercial_efficiency.csv")
        if efficiency is not None:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Commercial Rank",
                x=efficiency["team_canonical"],
                y=efficiency["commercial_rank"],
                marker_color="#E8002D",
            ))
            fig.add_trace(go.Bar(
                name="Performance Rank",
                x=efficiency["team_canonical"],
                y=efficiency["performance_rank"],
                marker_color="#1E41FF",
            ))
            fig.update_layout(
                barmode="group",
                title="Commercial Rank vs Performance Rank (lower = better)",
                xaxis_tickangle=-30,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Gap analysis:** Positive gap = commercially outperforms results | Negative gap = underperforming commercially")
            st.dataframe(
                efficiency[["team_canonical", "avg_championship_position", "avg_valuation_usd_m", "commercial_vs_performance_gap", "instagram_followers_m"]]
                .sort_values("commercial_vs_performance_gap", ascending=False)
                .rename(columns={
                    "team_canonical": "Team",
                    "avg_championship_position": "Avg WCC Pos",
                    "avg_valuation_usd_m": "Avg Valuation ($M)",
                    "commercial_vs_performance_gap": "Commercial vs Perf Gap",
                    "instagram_followers_m": "Instagram (M)",
                }),
                use_container_width=True,
                hide_index=True,
            )
        else:
            missing_data_warning("Team commercial efficiency data")

# ---------------------------------------------------------------------------
# Sponsorship ROI
# ---------------------------------------------------------------------------

elif section == "Sponsorship ROI":
    st.title("Sponsorship ROI")
    st.caption("How does F1 stack up as a marketing vehicle vs. other major sports?")

    tab1, tab2 = st.tabs(["Cross-Sport CPM", "F1 Deal Breakdown"])

    with tab1:
        with st.expander("📐 How CPM is estimated here", expanded=False):
            st.markdown("""
            ### Methodology

            **CPM (Cost Per Mille)** = cost to reach 1,000 viewers. It is the standard metric
            used across advertising and sports marketing to compare the efficiency of different
            media buys.

            **Formula used:**
            ```
            CPM = (Sponsorship or Ad Buy Cost / Total Viewers Reached) × 1,000
            ```

            **For F1 specifically**, the implied CPM is estimated using:
            - Average per-race global viewership (70–76M range, 2022–2025 FOM data)
            - Reported title sponsorship deal values (e.g. LVMH at ~$150M/season, Oracle/Red Bull at ~$100M/yr)
            - Estimated sponsor brand exposure as ~15% of total race viewership per race
              (accounting for screen-time, logo visibility, and broadcast geography)
            - Multiplied by races in the deal year to give a **season-level** total exposure figure
            - Season CPM = Annual Deal Value ÷ (Per-Race Exposure × Races) × 1,000

            **Benchmark CPMs** for other sports are sourced from Nielsen (NFL, NBA),
            industry reports, and SportsPro estimates. All figures are approximations —
            actual CPMs vary significantly by:
            - Placement type (title sponsor vs. sleeve vs. car livery)
            - Geography (US slots cost more than emerging markets)
            - Deal structure (race-by-race vs. season-long vs. multi-year)
            - Activation rights included (hospitality, digital, merchandise)

            **Use these numbers for directional comparison only**, not as a basis for
            negotiating an actual sponsorship contract.
            """)

        cpm = load("sports_cpm_comparison.csv")
        if cpm is not None:
            fig = px.bar(
                cpm.sort_values("cpm_usd"),
                x="cpm_usd", y="sport",
                orientation="h",
                title="Estimated CPM by Sport (USD per 1,000 viewers)",
                labels={"cpm_usd": "CPM (USD)", "sport": ""},
                color="cpm_usd",
                color_continuous_scale="RdYlGn_r",
                text="cpm_usd",
            )
            fig.update_traces(texttemplate="$%{text:.0f}", textposition="outside")
            fig.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

            st.info("""
            **CPM (Cost Per Mille)** = cost to reach 1,000 viewers. Lower CPM = more efficient reach.
            F1's global distribution makes it competitive on CPM despite higher total deal values.
            Note: CPM figures are industry estimates and vary significantly by placement, market, and deal structure.
            """)
            st.caption("⚠️ The CPM figures on this chart are **broadcast advertising rates** (buying airtime). The implied CPMs in the Deal Breakdown tab are **title sponsorship rates** — a fundamentally different product that includes logo rights, hospitality, and activation. They are not directly comparable.")
            st.dataframe(cpm[["sport", "cpm_usd", "avg_viewers_per_event_m", "source"]], use_container_width=True, hide_index=True)
        else:
            missing_data_warning("CPM comparison data")

    with tab2:
        deals = load("sponsorship_roi.csv")
        if deals is not None:
            fig = px.bar(
                deals.dropna(subset=["annual_value_usd_m"]).sort_values("annual_value_usd_m", ascending=False),
                x="sponsor", y="annual_value_usd_m",
                color="confidence",
                title="Reported F1 Sponsorship Deal Values (Annual USD M)",
                labels={"annual_value_usd_m": "Est. Annual Value ($M)", "sponsor": "Sponsor", "confidence": "Confidence"},
                color_discrete_map={"HIGH": "#2ECC71", "MED": "#F39C12", "LOW": "#E74C3C"},
                text="annual_value_usd_m",
            )
            fig.update_traces(texttemplate="$%{text:.0f}M", textposition="outside")
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            st.warning("**Transparency note:** Sponsorship values are estimated from public reports (SportsPro, Reuters, press releases). Many deals are confidential. Confidence levels: HIGH = confirmed multi-source, MED = single reliable source, LOW = industry estimate.")
            st.dataframe(
                deals[["sponsor", "team_or_entity", "deal_type", "annual_value_usd_m", "confidence", "source", "notes"]]
                .sort_values("annual_value_usd_m", ascending=False),
                use_container_width=True,
                hide_index=True,
            )
        else:
            missing_data_warning("Sponsorship ROI data")

# ---------------------------------------------------------------------------
# Scenario Modeler
# ---------------------------------------------------------------------------

elif section == "Scenario Modeler":
    st.title("Scenario Modeler")
    st.caption("How does championship outcome affect a team's estimated commercial value?")

    with st.expander("📐 How this model works", expanded=False):
        st.markdown("""
        ### Methodology

        This model uses **Ordinary Least Squares (OLS) linear regression** — one of the most standard
        statistical tools — to estimate the historical relationship between a team's WCC finishing position
        and its independently-estimated valuation (source: Sportico).

        **Step 1 — Find the historical slope**

        Using all available team-season data points (e.g. Ferrari P3 in 2023 at $3.13B, McLaren P1 in 2025 at $4.73B),
        we fit a regression line: `valuation = intercept + slope × position`. The slope is negative —
        better positions (lower numbers) correlate with higher valuations.

        **Step 2 — Apply to each team**

        For each scenario, the model calculates:
        ```
        Modeled Valuation = Base Valuation + (Scenario Position − 5) × Slope
        ```
        Position 5 is used as the "neutral" midfield anchor. A team projected to finish P1 gets
        a positive delta; a team projected at P8 gets a negative delta. A floor of 50% of base
        valuation prevents extreme downward outliers.

        **What the R² means**

        The R² value (shown below the chart) measures how much of the variation in team valuations
        is explained by championship position alone. The current model R² is shown live beneath the
        chart. Typically in this dataset position explains roughly 40–60% of valuation differences —
        the rest comes from brand heritage, ownership, engine partnerships, and market timing.

        **Limitations (important)**
        - This is a correlation-based projection, not a causal model. Ferrari's valuation reflects
          a century of brand equity, not just finishing position.
        - The model assumes the past relationship between position and valuation continues to hold.
        - Real-world valuation changes also depend on: driver contracts, regulation changes, ownership
          deals, sponsorship negotiations, and macroeconomic conditions.
        - All base valuations are Sportico estimates using revenue-multiple methodology — they are
          not audited financial figures.
        """)

    scenarios = load("valuation_scenarios.csv")
    if scenarios is not None:
        teams = sorted(scenarios["team"].unique())
        selected_teams = st.multiselect("Select teams to compare", teams, default=teams[:4])

        if selected_teams:
            filtered = scenarios[scenarios["team"].isin(selected_teams)]
            fig = px.bar(
                filtered,
                x="scenario", y="modeled_valuation_usd_m",
                color="team",
                barmode="group",
                title="Modeled Valuation by Championship Outcome (USD M)",
                labels={"modeled_valuation_usd_m": "Modeled Valuation ($M)", "scenario": "Scenario"},
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()
            st.subheader("Value at stake by scenario")
            pivot = filtered.pivot_table(index="team", columns="scenario", values="modeled_valuation_usd_m").reset_index()
            if "Win WCC (P1)" in pivot.columns and "Bottom Half (P8)" in pivot.columns:
                pivot["Upside (P1 vs P8, $M)"] = pivot["Win WCC (P1)"] - pivot["Bottom Half (P8)"]
            st.dataframe(pivot, use_container_width=True, hide_index=True)

            r2 = scenarios["r_squared"].dropna().iloc[0] if "r_squared" in scenarios.columns else None
            if r2 is not None:
                st.caption(f"Model R² = {r2:.2f} — {'strong' if r2 > 0.6 else 'moderate' if r2 > 0.3 else 'weak'} correlation between position and valuation in the dataset.")
            st.info("Base valuations are the most recent Sportico estimates (2025). The model extrapolates from the historical position-to-valuation correlation using all years with complete data. Real-world shifts depend on many additional factors beyond position.")
    else:
        missing_data_warning("Scenario model data")
