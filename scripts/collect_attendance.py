"""
Collects/compiles race attendance and ticket pricing data for F1 circuits.

Two modes:
  1. Scrape Wikipedia race attendance tables (best-effort)
  2. Load and validate the manual attendance template

Run: python scripts/collect_attendance.py
Outputs to: data/raw/attendance/
"""

import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

OUTPUT_DIR = Path("data/raw/attendance")
TEMPLATE_PATH = Path("data/templates/attendance.csv")

WIKIPEDIA_PAGES = {
    "Bahrain Grand Prix": "https://en.wikipedia.org/wiki/Bahrain_Grand_Prix",
    "Saudi Arabian Grand Prix": "https://en.wikipedia.org/wiki/Saudi_Arabian_Grand_Prix",
    "Australian Grand Prix": "https://en.wikipedia.org/wiki/Australian_Grand_Prix",
    "Chinese Grand Prix": "https://en.wikipedia.org/wiki/Chinese_Grand_Prix",
    "Miami Grand Prix": "https://en.wikipedia.org/wiki/Miami_Grand_Prix",
    "Monaco Grand Prix": "https://en.wikipedia.org/wiki/Monaco_Grand_Prix",
    "Canadian Grand Prix": "https://en.wikipedia.org/wiki/Canadian_Grand_Prix",
    "Spanish Grand Prix": "https://en.wikipedia.org/wiki/Spanish_Grand_Prix",
    "British Grand Prix": "https://en.wikipedia.org/wiki/British_Grand_Prix",
    "Hungarian Grand Prix": "https://en.wikipedia.org/wiki/Hungarian_Grand_Prix",
    "Belgian Grand Prix": "https://en.wikipedia.org/wiki/Belgian_Grand_Prix",
    "Dutch Grand Prix": "https://en.wikipedia.org/wiki/Dutch_Grand_Prix",
    "Italian Grand Prix": "https://en.wikipedia.org/wiki/Italian_Grand_Prix",
    "Singapore Grand Prix": "https://en.wikipedia.org/wiki/Singapore_Grand_Prix",
    "Japanese Grand Prix": "https://en.wikipedia.org/wiki/Japanese_Grand_Prix",
    "United States Grand Prix": "https://en.wikipedia.org/wiki/United_States_Grand_Prix",
    "Mexico City Grand Prix": "https://en.wikipedia.org/wiki/Mexico_City_Grand_Prix",
    "São Paulo Grand Prix": "https://en.wikipedia.org/wiki/S%C3%A3o_Paulo_Grand_Prix",
    "Las Vegas Grand Prix": "https://en.wikipedia.org/wiki/Las_Vegas_Grand_Prix",
    "Abu Dhabi Grand Prix": "https://en.wikipedia.org/wiki/Abu_Dhabi_Grand_Prix",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (research project, educational use)"}


def scrape_race_attendance(race_name: str, url: str) -> list[dict]:
    """Attempt to extract attendance figures from a Wikipedia race page."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        records = []

        for table in soup.find_all("table", class_="wikitable"):
            headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
            if not any("attend" in h for h in headers):
                continue
            try:
                attend_idx = next(i for i, h in enumerate(headers) if "attend" in h)
                year_idx = next((i for i, h in enumerate(headers) if "year" in h or "season" in h), 0)
            except StopIteration:
                continue

            for row in table.find_all("tr")[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) <= max(attend_idx, year_idx):
                    continue
                year_text = cells[year_idx].get_text(strip=True)
                attend_text = cells[attend_idx].get_text(strip=True).replace(",", "").replace(".", "")
                try:
                    year = int(year_text[:4])
                    attendance = int("".join(filter(str.isdigit, attend_text)))
                    if 2018 <= year <= 2024 and attendance > 0:
                        records.append({"race_name": race_name, "year": year, "attendance": attendance})
                except (ValueError, TypeError):
                    continue
        return records
    except Exception as e:
        print(f"  Could not scrape {race_name}: {e}")
        return []


def run_scrape():
    all_records = []
    print("Scraping Wikipedia for race attendance data...")
    for race_name, url in WIKIPEDIA_PAGES.items():
        print(f"  {race_name}...")
        records = scrape_race_attendance(race_name, url)
        all_records.extend(records)

    if all_records:
        df = pd.DataFrame(all_records).drop_duplicates().sort_values(["race_name", "year"])
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUTPUT_DIR / "attendance_scraped.csv", index=False)
        print(f"Saved {len(df)} records -> attendance_scraped.csv")
    else:
        print("No structured attendance data found via scraping. Use the manual template.")

    return all_records


def validate_template():
    if not TEMPLATE_PATH.exists():
        print(f"Template not found at {TEMPLATE_PATH}. Run create_templates.py first.")
        return
    df = pd.read_csv(TEMPLATE_PATH)
    missing = df[df["attendance"].isna() | (df["attendance"] == 0)]
    if not missing.empty:
        print(f"  {len(missing)} rows still need attendance values:")
        print(missing[["race_name", "year"]].to_string(index=False))
    else:
        print("Template is complete.")
    df.to_csv(OUTPUT_DIR / "attendance_final.csv", index=False)
    print(f"Saved validated template -> attendance_final.csv")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_scrape()
    print("\nDone. Review data/raw/attendance/ and fill any gaps with the manual template.")
