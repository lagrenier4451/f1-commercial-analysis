"""
Collects F1 constructor standings, driver standings, and race results
from the Jolpica API (community Ergast mirror) for 2014-2025.

Run: python scripts/collect_f1_standings.py
Outputs to: data/raw/standings/
"""

import requests
import pandas as pd
import time
from pathlib import Path
from tqdm import tqdm

BASE_URL = "https://api.jolpi.ca/ergast/f1"
OUTPUT_DIR = Path("data/raw/standings")
YEARS = range(2014, 2026)  # 2014 = pre-Liberty baseline; 2025 = latest complete season


def get_json(url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"  Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(2)
    return None


def collect_constructor_standings():
    records = []
    print("Collecting constructor standings...")
    for year in tqdm(YEARS):
        data = get_json(f"{BASE_URL}/{year}/constructorStandings.json")
        if not data:
            continue
        standings_list = data["MRData"]["StandingsTable"]["StandingsLists"]
        if not standings_list:
            continue
        for entry in standings_list[0]["ConstructorStandings"]:
            records.append({
                "year": year,
                "position": int(entry["position"]),
                "points": float(entry["points"]),
                "wins": int(entry["wins"]),
                "constructor_id": entry["Constructor"]["constructorId"],
                "constructor_name": entry["Constructor"]["name"],
                "nationality": entry["Constructor"]["nationality"],
            })
        time.sleep(0.3)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_DIR / "constructor_standings.csv", index=False)
    print(f"  Saved {len(df)} rows -> constructor_standings.csv")
    return df


def collect_driver_standings():
    records = []
    print("Collecting driver standings...")
    for year in tqdm(YEARS):
        data = get_json(f"{BASE_URL}/{year}/driverStandings.json")
        if not data:
            continue
        standings_list = data["MRData"]["StandingsTable"]["StandingsLists"]
        if not standings_list:
            continue
        for entry in standings_list[0]["DriverStandings"]:
            driver = entry["Driver"]
            constructor = entry["Constructors"][0] if entry["Constructors"] else {}
            records.append({
                "year": year,
                "position": int(entry.get("position", 0)),
                "points": float(entry.get("points", 0)),
                "wins": int(entry.get("wins", 0)),
                "driver_id": driver.get("driverId"),
                "driver_name": f"{driver.get('givenName')} {driver.get('familyName')}",
                "nationality": driver.get("nationality"),
                "constructor_id": constructor.get("constructorId"),
                "constructor_name": constructor.get("name"),
            })
        time.sleep(0.3)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_DIR / "driver_standings.csv", index=False)
    print(f"  Saved {len(df)} rows -> driver_standings.csv")
    return df


def collect_race_results():
    records = []
    print("Collecting race results...")
    for year in tqdm(YEARS):
        page, offset = 0, 0
        while True:
            data = get_json(f"{BASE_URL}/{year}/results.json?limit=100&offset={offset}")
            if not data:
                break
            races = data["MRData"]["RaceTable"]["Races"]
            if not races:
                break
            for race in races:
                for result in race["Results"]:
                    driver = result["Driver"]
                    constructor = result["Constructor"]
                    records.append({
                        "year": year,
                        "round": int(race["round"]),
                        "race_name": race["raceName"],
                        "circuit": race["Circuit"]["circuitName"],
                        "country": race["Circuit"]["Location"]["country"],
                        "date": race["date"],
                        "driver_id": driver["driverId"],
                        "driver_name": f"{driver['givenName']} {driver['familyName']}",
                        "constructor_id": constructor["constructorId"],
                        "constructor_name": constructor["name"],
                        "grid": int(result.get("grid", 0)),
                        "position": result.get("position"),
                        "points": float(result.get("points", 0)),
                        "laps": int(result.get("laps", 0)),
                        "status": result.get("status"),
                    })
            total = int(data["MRData"]["total"])
            offset += 100
            if offset >= total:
                break
            time.sleep(0.3)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_DIR / "race_results.csv", index=False)
    print(f"  Saved {len(df)} rows -> race_results.csv")
    return df


def collect_race_schedule():
    records = []
    print("Collecting race schedules...")
    for year in tqdm(YEARS):
        data = get_json(f"{BASE_URL}/{year}.json")
        if not data:
            continue
        for race in data["MRData"]["RaceTable"]["Races"]:
            records.append({
                "year": year,
                "round": int(race["round"]),
                "race_name": race["raceName"],
                "circuit_id": race["Circuit"]["circuitId"],
                "circuit_name": race["Circuit"]["circuitName"],
                "locality": race["Circuit"]["Location"]["locality"],
                "country": race["Circuit"]["Location"]["country"],
                "date": race["date"],
            })
        time.sleep(0.3)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_DIR / "race_schedule.csv", index=False)
    print(f"  Saved {len(df)} rows -> race_schedule.csv")
    return df


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    collect_constructor_standings()
    collect_driver_standings()
    collect_race_results()
    collect_race_schedule()
    print("\nDone. All standings data saved to data/raw/standings/")
