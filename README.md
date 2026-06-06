# The Business of Speed
### A Data-Driven Analysis of F1's Commercial Value (2014–2024)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://f1-commercial-analysis-lag-2026.streamlit.app/)

Formula 1 is no longer just a motorsport — it's a global media and marketing property. In 2017, Liberty Media acquired F1 from Bernie Ecclestone. What followed is one of sport's most dramatic commercial turnarounds: from a viewership trough of 352M (2017) to 6.5M race-day attendees, billion-dollar team valuations, and the most valuable sponsorship roster in motorsport history.

This project quantifies that transformation across three analytical pillars.

---

## What's Inside

| Pillar | Question Answered |
|--------|------------------|
| 📈 **F1's Growth Story** | How much did viewership and attendance grow — and where did it bottom out? |
| 🏆 **Team Commercial Value** | Which teams win off-track, and does championship performance drive valuation? |
| 💰 **Sponsorship ROI** | Is F1 a good marketing vehicle vs. other major sports? |

---

## Project Structure

```
f1-commercial-analysis/
├── data/
│   ├── templates/        ← Verified, sourced datasets (viewership, attendance, valuations, etc.)
│   └── raw/              ← API-pulled race data (generated, not committed)
├── scripts/
│   ├── collect_f1_standings.py   ← Pulls constructor/driver standings from Jolpica API (2014-2024)
│   ├── collect_attendance.py     ← Scrapes/validates race attendance data
│   ├── create_templates.py       ← One-time template initialiser (skip-if-exists)
│   ├── analyze.py                ← Core analysis: growth, valuations, ROI, scenarios
│   └── data_utils.py             ← Shared loading & preprocessing utilities
├── dashboard/
│   └── app.py            ← Streamlit interactive dashboard
├── report/               ← Written report (in progress)
└── requirements.txt
```

---

## Data Sources

| Dataset | Source | Confidence |
|---------|--------|------------|
| Constructor & driver standings | [Jolpica F1 API](https://api.jolpi.ca/ergast/f1/) | Verified |
| Race attendance (145 races) | [GPDestinations.com](https://gpdestinations.com/resources/f1-attendance-figures/) | Verified |
| Global viewership | [Formulapedia](https://formulapedia.com/f1-statistics/) / FOM press releases | Verified |
| US viewership (ESPN/Nielsen) | [Motorsport.com](https://www.motorsport.com) / [Blackbook Motorsport](https://www.blackbookmotorsport.com) | Verified |
| Team valuations | [Sportico](https://www.sportico.com) (2023 & 2024 reports) | Verified |
| Sponsorship deal values | SportsPro, Reuters, GlobalData, press releases | Reported estimates — confidence labeled per row |

> **Transparency note:** Sponsorship values are sourced from public reporting. Many F1 deals are confidential. Every figure in `data/templates/` includes its source and a confidence rating (HIGH / MED / LOW).

---

## Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pull F1 standings data (2014-2024) from the Jolpica API
python scripts/collect_f1_standings.py

# 3. Run the analysis
python scripts/analyze.py

# 4. Launch the dashboard
streamlit run dashboard/app.py
```

---

## Dashboard Sections

- **Overview** — headline metrics and the full viewership arc with Liberty Media acquisition marker
- **F1's Growth Story** — viewership 2014–2024, attendance by circuit, social media growth
- **Team Commercial Value** — valuation vs. championship position, commercial efficiency rankings
- **Sponsorship ROI** — CPM comparison across sports, deal breakdown by confidence level
- **Scenario Modeler** — model how championship outcomes shift team valuations (R²=0.53)

---

## Methodology Notes

- **Viewership (2014–2021):** FOM "unique viewer" metric counts any individual who watched any part of any race globally. Methodology is disputed; used for trend direction.
- **Viewership (2022+):** FOM switched to cumulative reporting (total views across all races). Not directly comparable to the earlier series.
- **Team valuations:** Sportico uses a revenue-multiple methodology. Figures are estimates, not audited financials.
- **Attendance:** GPDestinations aggregates circuit-reported figures. Counting methodology is not standardised across circuits.

---

*Built with Python, Pandas, Plotly, and Streamlit.*
