"""
Creates manual data entry templates pre-populated with known/reported values.
Sources are cited inline. Figures marked ESTIMATE should be verified before publishing.

Run: python scripts/create_templates.py
Outputs to: data/templates/
"""

import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("data/templates")


def create_viewership_template():
    """
    Global cumulative unique TV viewers per season.
    Source: FOM press releases, SportsPro Media, Formula1.com newsroom.
    US figures: Nielsen/ESPN ratings reports.
    """
    data = [
        {"year": 2018, "global_unique_viewers_m": 490.0, "us_avg_viewers_per_race_k": 547, "yoy_growth_pct": None, "source": "FOM Press Release", "notes": "Pre-Drive to Survive baseline"},
        {"year": 2019, "global_unique_viewers_m": 471.0, "us_avg_viewers_per_race_k": 903, "yoy_growth_pct": -3.9, "source": "FOM Press Release", "notes": "DtS S1 released Mar 2019; US growth via ABC deals"},
        {"year": 2020, "global_unique_viewers_m": 433.0, "us_avg_viewers_per_race_k": 1100, "yoy_growth_pct": -8.1, "source": "FOM Press Release", "notes": "COVID season, 17 races vs 21; shorter calendar depresses total"},
        {"year": 2021, "global_unique_viewers_m": 445.0, "us_avg_viewers_per_race_k": 1300, "yoy_growth_pct": 2.8, "source": "FOM Press Release", "notes": "DtS effect accelerating; Verstappen/Hamilton title fight"},
        {"year": 2022, "global_unique_viewers_m": 517.0, "us_avg_viewers_per_race_k": 1260, "yoy_growth_pct": 16.2, "source": "FOM Press Release", "notes": "Record at time; Miami GP debut"},
        {"year": 2023, "global_unique_viewers_m": 595.0, "us_avg_viewers_per_race_k": 1110, "yoy_growth_pct": 15.1, "source": "FOM / Estimated", "notes": "ESTIMATE - FOM reported 'record audiences'; Las Vegas GP debut"},
        {"year": 2024, "global_unique_viewers_m": None, "us_avg_viewers_per_race_k": None, "yoy_growth_pct": None, "source": "NEEDS DATA", "notes": "Fill when FOM 2024 report published"},
    ]
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "viewership.csv", index=False)
    print(f"  Created viewership.csv ({len(df)} rows)")


def create_team_valuations_template():
    """
    F1 team franchise valuations.
    Source: Forbes 'Most Valuable F1 Teams' annual list.
    Note: Forbes uses a proprietary methodology. Treat as estimates.
    """
    data = [
        {"year": 2022, "team": "Ferrari", "valuation_usd_m": 3300, "revenue_usd_m": 657, "operating_income_usd_m": 100, "source": "Forbes 2022", "notes": "Scuderia Ferrari entity only"},
        {"year": 2022, "team": "Mercedes-AMG Petronas", "valuation_usd_m": 2100, "revenue_usd_m": 556, "operating_income_usd_m": 78, "source": "Forbes 2022", "notes": ""},
        {"year": 2022, "team": "Red Bull Racing", "valuation_usd_m": 2000, "revenue_usd_m": 502, "operating_income_usd_m": 88, "source": "Forbes 2022", "notes": ""},
        {"year": 2022, "team": "McLaren Racing", "valuation_usd_m": 1100, "revenue_usd_m": 289, "operating_income_usd_m": 28, "source": "Forbes 2022", "notes": ""},
        {"year": 2022, "team": "Alpine F1 Team", "valuation_usd_m": 900, "revenue_usd_m": 263, "operating_income_usd_m": 22, "source": "Forbes 2022", "notes": ""},
        {"year": 2022, "team": "Aston Martin F1", "valuation_usd_m": 800, "revenue_usd_m": 185, "operating_income_usd_m": 11, "source": "Forbes 2022", "notes": ""},
        {"year": 2022, "team": "Williams Racing", "valuation_usd_m": 600, "revenue_usd_m": 163, "operating_income_usd_m": 8, "source": "Forbes 2022", "notes": ""},
        {"year": 2023, "team": "Ferrari", "valuation_usd_m": 3800, "revenue_usd_m": None, "operating_income_usd_m": None, "source": "Forbes 2023 ESTIMATE", "notes": "ESTIMATE - verify with Forbes 2023 report"},
        {"year": 2023, "team": "Red Bull Racing", "valuation_usd_m": 3000, "revenue_usd_m": None, "operating_income_usd_m": None, "source": "Forbes 2023 ESTIMATE", "notes": "ESTIMATE"},
        {"year": 2023, "team": "Mercedes-AMG Petronas", "valuation_usd_m": 2700, "revenue_usd_m": None, "operating_income_usd_m": None, "source": "Forbes 2023 ESTIMATE", "notes": "ESTIMATE"},
        {"year": 2023, "team": "McLaren Racing", "valuation_usd_m": 1500, "revenue_usd_m": None, "operating_income_usd_m": None, "source": "Forbes 2023 ESTIMATE", "notes": "ESTIMATE"},
        {"year": 2023, "team": "Aston Martin F1", "valuation_usd_m": 1000, "revenue_usd_m": None, "operating_income_usd_m": None, "source": "Forbes 2023 ESTIMATE", "notes": "ESTIMATE"},
    ]
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "team_valuations.csv", index=False)
    print(f"  Created team_valuations.csv ({len(df)} rows)")


def create_sponsorship_template():
    """
    Known/reported sponsorship deal values.
    Sources: SportsPro Media, Racefans.net, press releases, Reuters.
    Confidence: HIGH = confirmed by multiple sources, MED = single source/estimated, LOW = rumored range.
    """
    data = [
        # F1-level (Liberty Media / FOM deals)
        {"year_start": 2020, "year_end": 2030, "team_or_entity": "Formula 1 (FOM)", "sponsor": "Aramco", "deal_type": "Global Partner", "annual_value_usd_m": 50.0, "confidence": "MED", "source": "SportsPro / Reuters", "notes": "Multi-year global partner deal; exact value undisclosed"},
        {"year_start": 2020, "year_end": 2025, "team_or_entity": "Formula 1 (FOM)", "sponsor": "DHL", "deal_type": "Official Logistics Partner", "annual_value_usd_m": 30.0, "confidence": "LOW", "source": "Industry estimate", "notes": "Longstanding partner; value estimated"},
        {"year_start": 2024, "year_end": 2034, "team_or_entity": "Formula 1 (FOM)", "sponsor": "LVMH", "deal_type": "Global Partner", "annual_value_usd_m": 15.0, "confidence": "MED", "source": "Reuters - €150M over 10yr reported", "notes": "€150M/10yr = ~€15M/yr; covers Rolex replacement and Louis Vuitton"},
        # Team-level deals
        {"year_start": 2021, "year_end": 2026, "team_or_entity": "Red Bull Racing", "sponsor": "Oracle", "deal_type": "Title Sponsor", "annual_value_usd_m": 50.0, "confidence": "MED", "source": "SportsPro / multiple reports", "notes": "Oracle Red Bull Racing naming rights; $500M over reported period = ~$50M/yr"},
        {"year_start": 2020, "year_end": 2025, "team_or_entity": "Mercedes-AMG Petronas", "sponsor": "Petronas", "deal_type": "Title Sponsor", "annual_value_usd_m": 50.0, "confidence": "MED", "source": "Industry reports", "notes": "Longstanding; ~$50M/yr estimated"},
        {"year_start": 2020, "year_end": 2025, "team_or_entity": "Mercedes-AMG Petronas", "sponsor": "Ineos", "deal_type": "Principal Partner", "annual_value_usd_m": 35.0, "confidence": "LOW", "source": "Estimate", "notes": "Ineos took equity stake; cash value unclear"},
        {"year_start": 2023, "year_end": 2026, "team_or_entity": "Mercedes-AMG Petronas", "sponsor": "HP", "deal_type": "Principal Partner", "annual_value_usd_m": 30.0, "confidence": "LOW", "source": "Estimate", "notes": "HP Piper branding; deal value not disclosed"},
        {"year_start": 2022, "year_end": 2027, "team_or_entity": "Ferrari", "sponsor": "Santander", "deal_type": "Principal Partner", "annual_value_usd_m": 35.0, "confidence": "LOW", "source": "Estimate", "notes": "Historical Santander/Ferrari relationship"},
        {"year_start": 2021, "year_end": 2025, "team_or_entity": "Ferrari", "sponsor": "Mission Winnow/Philip Morris", "deal_type": "Title/Principal", "annual_value_usd_m": 40.0, "confidence": "LOW", "source": "Various reports - controversial", "notes": "Arrangement has varied by market/regulation"},
        {"year_start": 2024, "year_end": 2028, "team_or_entity": "Ferrari", "sponsor": "HP", "deal_type": "Title Sponsor", "annual_value_usd_m": 90.0, "confidence": "HIGH", "source": "Ferrari Press Release / SportsPro", "notes": "Scuderia Ferrari HP; reported ~$90M/yr - largest team-level deal"},
        {"year_start": 2021, "year_end": 2025, "team_or_entity": "McLaren Racing", "sponsor": "Gulf Oil", "deal_type": "Partner", "annual_value_usd_m": 10.0, "confidence": "LOW", "source": "Estimate", "notes": "Heritage livery partner; value unclear"},
        {"year_start": 2023, "year_end": 2028, "team_or_entity": "McLaren Racing", "sponsor": "Google / Chrome", "deal_type": "Principal Partner", "annual_value_usd_m": 40.0, "confidence": "MED", "source": "Multiple reports", "notes": "Chrome branding on MCL cars"},
        {"year_start": 2023, "year_end": None, "team_or_entity": "Aston Martin F1", "sponsor": "Aramco", "deal_type": "Title Sponsor", "annual_value_usd_m": 30.0, "confidence": "LOW", "source": "Estimate", "notes": "Aston Martin Aramco F1 team naming"},
        {"year_start": 2024, "year_end": None, "team_or_entity": "Williams Racing", "sponsor": "Sartorius", "deal_type": "Principal Partner", "annual_value_usd_m": 15.0, "confidence": "LOW", "source": "Estimate", "notes": ""},
    ]
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "sponsorship_values.csv", index=False)
    print(f"  Created sponsorship_values.csv ({len(df)} rows)")


def create_attendance_template():
    """
    Race weekend attendance (3-day total where available, else race day).
    Sources: Circuit press releases, FOM, local reports.
    """
    data = [
        {"year": 2019, "race_name": "British Grand Prix", "circuit": "Silverstone", "country": "UK", "attendance_3day": 351000, "attendance_race_day": 141000, "source": "Silverstone Circuit", "notes": ""},
        {"year": 2022, "race_name": "British Grand Prix", "circuit": "Silverstone", "country": "UK", "attendance_3day": 420114, "attendance_race_day": 142000, "source": "Silverstone Circuit", "notes": "Post-COVID record"},
        {"year": 2023, "race_name": "British Grand Prix", "circuit": "Silverstone", "country": "UK", "attendance_3day": 480000, "attendance_race_day": None, "source": "Silverstone Circuit ESTIMATE", "notes": "ESTIMATE"},
        {"year": 2022, "race_name": "Miami Grand Prix", "circuit": "Miami International Autodrome", "country": "USA", "attendance_3day": 240000, "attendance_race_day": 80000, "source": "F1 Press Release", "notes": "Inaugural race"},
        {"year": 2023, "race_name": "Miami Grand Prix", "circuit": "Miami International Autodrome", "country": "USA", "attendance_3day": 275000, "attendance_race_day": None, "source": "F1 Press Release", "notes": ""},
        {"year": 2023, "race_name": "Las Vegas Grand Prix", "circuit": "Las Vegas Strip Circuit", "country": "USA", "attendance_3day": 315000, "attendance_race_day": 105000, "source": "F1 Press Release", "notes": "Inaugural race"},
        {"year": 2019, "race_name": "United States Grand Prix", "circuit": "Circuit of the Americas", "country": "USA", "attendance_3day": 268000, "attendance_race_day": 104000, "source": "COTA", "notes": ""},
        {"year": 2021, "race_name": "United States Grand Prix", "circuit": "Circuit of the Americas", "country": "USA", "attendance_3day": 400000, "attendance_race_day": 140000, "source": "COTA", "notes": "Post-COVID return, high demand"},
        {"year": 2022, "race_name": "United States Grand Prix", "circuit": "Circuit of the Americas", "country": "USA", "attendance_3day": 440000, "attendance_race_day": 145000, "source": "COTA", "notes": ""},
        {"year": 2023, "race_name": "United States Grand Prix", "circuit": "Circuit of the Americas", "country": "USA", "attendance_3day": 440000, "attendance_race_day": None, "source": "COTA ESTIMATE", "notes": "ESTIMATE"},
        {"year": 2022, "race_name": "Australian Grand Prix", "circuit": "Albert Park", "country": "Australia", "attendance_3day": 419114, "attendance_race_day": 134000, "source": "AGP Corporation", "notes": "New 3-day record"},
        {"year": 2023, "race_name": "Australian Grand Prix", "circuit": "Albert Park", "country": "Australia", "attendance_3day": 444631, "attendance_race_day": 136000, "source": "AGP Corporation", "notes": "All-time record"},
        {"year": 2022, "race_name": "Dutch Grand Prix", "circuit": "Circuit Zandvoort", "country": "Netherlands", "attendance_3day": 305000, "attendance_race_day": 105000, "source": "Zandvoort Circuit", "notes": "Sold out; Verstappen home race"},
        {"year": 2023, "race_name": "Dutch Grand Prix", "circuit": "Circuit Zandvoort", "country": "Netherlands", "attendance_3day": 300000, "attendance_race_day": 100000, "source": "Zandvoort Circuit", "notes": "Sold out"},
        {"year": 2022, "race_name": "Italian Grand Prix", "circuit": "Monza", "country": "Italy", "attendance_3day": 332000, "attendance_race_day": 136000, "source": "Monza", "notes": ""},
        {"year": 2022, "race_name": "Mexican Grand Prix", "circuit": "Autodromo Hermanos Rodriguez", "country": "Mexico", "attendance_3day": 401677, "attendance_race_day": 133000, "source": "Mexico GP Organization", "notes": ""},
        {"year": 2023, "race_name": "Mexican Grand Prix", "circuit": "Autodromo Hermanos Rodriguez", "country": "Mexico", "attendance_3day": 389950, "attendance_race_day": None, "source": "Mexico GP Organization", "notes": ""},
        {"year": 2022, "race_name": "Brazilian Grand Prix", "circuit": "Interlagos", "country": "Brazil", "attendance_3day": 300000, "attendance_race_day": None, "source": "Various", "notes": "ESTIMATE"},
        {"year": 2022, "race_name": "Singapore Grand Prix", "circuit": "Marina Bay Street Circuit", "country": "Singapore", "attendance_3day": 302000, "attendance_race_day": None, "source": "Singapore Tourism Board", "notes": "Post-COVID return"},
        {"year": 2023, "race_name": "Singapore Grand Prix", "circuit": "Marina Bay Street Circuit", "country": "Singapore", "attendance_3day": 310000, "attendance_race_day": None, "source": "Singapore Tourism Board", "notes": ""},
    ]
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "attendance.csv", index=False)
    print(f"  Created attendance.csv ({len(df)} rows)")


def create_social_media_template():
    """
    Team social media follower counts (Instagram as primary metric).
    Source: Public Instagram profiles; year-end snapshots.
    """
    data = [
        {"year": 2023, "team": "Ferrari", "instagram_followers_m": 8.2, "youtube_subscribers_m": 2.1, "twitter_followers_m": 4.8, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Red Bull Racing", "instagram_followers_m": 12.5, "youtube_subscribers_m": 5.3, "twitter_followers_m": 6.1, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Mercedes-AMG Petronas", "instagram_followers_m": 6.8, "youtube_subscribers_m": 3.2, "twitter_followers_m": 4.1, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "McLaren Racing", "instagram_followers_m": 6.2, "youtube_subscribers_m": 2.8, "twitter_followers_m": 3.9, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Aston Martin F1", "instagram_followers_m": 2.1, "youtube_subscribers_m": 0.8, "twitter_followers_m": 1.5, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Alpine F1 Team", "instagram_followers_m": 1.8, "youtube_subscribers_m": 0.6, "twitter_followers_m": 1.2, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Williams Racing", "instagram_followers_m": 1.9, "youtube_subscribers_m": 0.7, "twitter_followers_m": 1.4, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Haas F1 Team", "instagram_followers_m": 1.4, "youtube_subscribers_m": 0.5, "twitter_followers_m": 1.0, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "Alfa Romeo / Sauber", "instagram_followers_m": 1.1, "youtube_subscribers_m": 0.3, "twitter_followers_m": 0.7, "source": "Public profiles Dec 2023", "notes": ""},
        {"year": 2023, "team": "AlphaTauri / RB", "instagram_followers_m": 1.0, "youtube_subscribers_m": 0.4, "twitter_followers_m": 0.8, "source": "Public profiles Dec 2023", "notes": ""},
        # F1 Official
        {"year": 2023, "team": "Formula 1 (official)", "instagram_followers_m": 33.5, "youtube_subscribers_m": 10.2, "twitter_followers_m": 12.0, "source": "Public profiles Dec 2023", "notes": "F1 official accounts"},
        {"year": 2018, "team": "Formula 1 (official)", "instagram_followers_m": 4.0, "youtube_subscribers_m": 1.2, "twitter_followers_m": 4.5, "source": "Estimate / various reports", "notes": "ESTIMATE - pre-DtS baseline"},
    ]
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "social_media.csv", index=False)
    print(f"  Created social_media.csv ({len(df)} rows)")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("NOTE: create_templates.py only writes files that do NOT already exist.")
    print("To force-overwrite, delete the target CSV first.\n")
    for fn, creator in [
        ("viewership.csv", create_viewership_template),
        ("team_valuations.csv", create_team_valuations_template),
        ("sponsorship_values.csv", create_sponsorship_template),
        ("attendance.csv", create_attendance_template),
        ("social_media.csv", create_social_media_template),
    ]:
        if (OUTPUT_DIR / fn).exists():
            print(f"  SKIP {fn} (already exists)")
        else:
            creator()
    print(f"\nDone.")
