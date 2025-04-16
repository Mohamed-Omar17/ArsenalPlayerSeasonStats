import requests

url = "https://api-football-v1.p.rapidapi.com/v3/players"

headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

all_players = []
page = 1
has_more = True

while has_more:
    querystring = {
        "team": "42",
        "season": "2024",
        "league": "39",
        "page": str(page)
    }

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

# Display player stats
for player in all_players:
    info = player['player']
    stats = player['statistics'][0]  # Premier League stats
    print(f"Name: {info['name']}")
    print(f"Goals: {stats['goals']['total']}")
    print(f"Assists: {stats['goals']['assists']}")
    print(f"Rating: {stats['games']['rating']}")
    print("-" * 30)
