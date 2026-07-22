import os
import json
import base64
import requests
import subprocess

COMLINK_URL = os.environ.get("COMLINK_URL", "")
GH_TOKEN = os.environ.get("GH_TOKEN", "")
MEMBRES_API_URL = "https://api.github.com/repos/Fullflam/swgoh-tracker/contents/membres.py"

SHIP_IDS = {
    "executor": "CAPITALEXECUTOR",
    "profundity": "CAPITALPROFUNDITY",
    "leviathan": "CAPITALLEVIATHAN"
}

def get_membres():
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    r = requests.get(MEMBRES_API_URL, headers=headers, timeout=15)
    r.raise_for_status()
    content = base64.b64decode(r.json()["content"]).decode("utf-8")
    namespace = {}
    exec(content, namespace)
    return namespace["MEMBRES"]

def get_ship_stars(player_id):
    r = requests.post(
        f"{COMLINK_URL}/player",
        json={"payload": {"playerId": player_id}, "enums": False},
        timeout=30
    )
    r.raise_for_status()
    data = r.json()
    stars = {"executor": 0, "profundity": 0, "leviathan": 0}
    for unit in data.get("rosterUnit", []):
        def_id = unit.get("definitionId", "").split(":")[0]
        for key, ship_id in SHIP_IDS.items():
            if def_id == ship_id:
                stars[key] = unit.get("currentRarity", 0)
    return stars

def main():
    membres = get_membres()
    result = {}
    for player_id in membres.keys():
        try:
            result[player_id] = get_ship_stars(player_id)
        except Exception as e:
            print(f"Erreur pour {player_id} : {e}")

    with open("vaisseau_stars.py", "w") as f:
        f.write("VAISSEAU_STARS = " + json.dumps(result, indent=4) + "\n")

    subprocess.run(["git", "config", "--local", "user.email", "action@github.com"])
    subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"])
    subprocess.run(["git", "add", "vaisseau_stars.py"])
    subprocess.run(["git", "commit", "-m", "Update vaisseau stars [auto]"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
