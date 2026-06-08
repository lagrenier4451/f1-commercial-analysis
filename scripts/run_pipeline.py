"""
Full data collection and analysis pipeline.
Run this once to generate all datasets before launching the dashboard.

Usage: python scripts/run_pipeline.py [--skip-api]
  --skip-api   Skip the Jolpica API calls (use if rate-limited or offline)
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS = Path(__file__).parent


def run(script: str, label: str):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        cwd=Path(__file__).parent.parent,
    )
    if result.returncode != 0:
        print(f"  ERROR: {script} failed with exit code {result.returncode}")
        return False
    return True


def main():
    skip_api = "--skip-api" in sys.argv
    success = True

    print("\nF1 Commercial Analysis — Data Pipeline")
    print("======================================")

    # Step 1: Create manual templates (always run first)
    success &= run("create_templates.py", "Step 1/4: Creating data templates")

    # Step 2: Fetch F1 API data
    if not skip_api:
        success &= run("collect_f1_standings.py", "Step 2/4: Collecting F1 standings from Jolpica API (2014-2025)")
    else:
        print("\nStep 2/4: Skipping API collection (--skip-api)")

    # Step 3: Scrape attendance data
    success &= run("collect_attendance.py", "Step 3/4: Collecting race attendance data")

    # Step 4: Run analyses
    success &= run("analyze.py", "Step 4/4: Running analyses and generating processed datasets")

    print("\n" + "="*60)
    if success:
        print("Pipeline complete.")
        print("Next steps:")
        print("  1. Review data/templates/ — all datasets are sourced; update if newer data is available")
        print("  2. Re-run if needed: python scripts/analyze.py")
        print("  3. Launch dashboard: streamlit run dashboard/app.py")
    else:
        print("Pipeline finished with errors. Check output above.")
    print("="*60)


if __name__ == "__main__":
    main()
