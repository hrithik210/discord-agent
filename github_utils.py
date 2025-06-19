import requests
from datetime import datetime, timedelta
import os

def get_today_commit_stats(username):
    today = datetime.utcnow().date()
    since = f"{today}T00:00:00Z"
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"Accept": "application/vnd.github.v3+json"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"added": 0, "removed": 0}

    data = resp.json()
    added, removed = 0, 0
    for event in data:
        if event["type"] == "PushEvent":
            for commit in event["payload"]["commits"]:
                commit_url = commit["url"].replace("api.", "").replace("repos/", "")
                commit_data = requests.get(f"https://api.github.com/repos/{username}/{event['repo']['name'].split('/')[1]}/commits/{commit['sha']}").json()
                stats = commit_data.get("stats", {})
                added += stats.get("additions", 0)
                removed += stats.get("deletions", 0)

    return {"added": added, "removed": removed}