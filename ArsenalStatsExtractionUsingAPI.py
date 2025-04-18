import csv
import requests

url = "https://api-football-v1.p.rapidapi.com/v3/players"

headers = {
    "X-RapidAPI-Key": "1537e87510mshf77ffb31d1a8b9fp1aadedjsned36317aaeec",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

all_players = []
page = 1
has_more = True

while has_more:
    querystring = {
        "team": "42",      # PSG
        "season": "2024",
        "league": "39"     # Premier League (make sure this matches team/season)
    }

    querystring["page"] = str(page)

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        break

    players = data.get('response', [])
    all_players.extend(players)

    total_pages = data.get("paging", {}).get("total", 1)
    has_more = page < total_pages
    page += 1

# Write to CSV
with open("players.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        "id", "name", "age", "nationality", "position",
        "team", "appearances", "goals", "assists", "rating"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for player in all_players:
        info = player['player']
        stats = player['statistics'][0]  # Assumes only one set of stats
        raw_rating = stats.get("games", {}).get("rating")
        rating = round(float(raw_rating), 2) if raw_rating else None

        total_appearances = stats.get("games", {}).get("appearences")

        if total_appearances:
            writer.writerow({
                "id": info.get("id"),
                "name": info.get("name"),
                "age": info.get("age"),
                "nationality": info.get("nationality"),
                "position": stats.get("games", {}).get("position"),
                "team": stats.get("team", {}).get("name"),
                "appearances": stats.get("games", {}).get("appearences"),
                "goals": stats.get("goals", {}).get("total"),
                "assists": stats.get("goals", {}).get("assists"),
                "rating": rating
            })
