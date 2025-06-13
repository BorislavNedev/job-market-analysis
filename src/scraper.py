# --------------------------------------
# scraper.py — Fetch jobs from RemoteOK
# --------------------------------------

import requests
import json
import os

def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # raise error if bad response
        jobs = response.json()
        return jobs[1:]  # first element is metadata
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []

def save_jobs_to_file(jobs, path="../data/jobs_raw.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4)

if __name__ == "__main__":
    jobs = fetch_remoteok_jobs()
    print(f"✅ Fetched {len(jobs)} job posts.")
    save_jobs_to_file(jobs)
    print("💾 Saved to data/jobs_raw.json")