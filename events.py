import requests
import os
from datetime import datetime, date, timedelta
from calendar import monthrange

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")
COMLINK_URL = os.environ.get("COMLINK_URL", "")
ALLY_CODE = os.environ.get("ALLY_CODE", "")

def dernier_jour_mois():
    aujourd_hui = date.today()
    return monthrange(aujourd_hui.year, aujourd_hui.month)[1]

def get_events():
    res = requests.post(
        f"{COMLINK_URL}/getEvents",
        json={"payload": {}, "enums": False},
        timeout=30
    )
    res.raise_for_status()
    return res.json().get("gameEvent", [])

def get_next_tb_date():
    try:
        joueur = requests.post(
            f"{COMLINK_URL}/player",
            json={"payload": {"allyCode": ALLY_CODE}, "enums": False},
            timeout=30
        )
        joueur.raise_for_status()
        guild_id = joueur.json().get("guildId")

        guilde = requests.post(
            f"{COMLINK_URL}/guild",
            json={"payload": {"guildId": guild_id}, "enums": False},
            timeout=30
        )
        guilde.raise_for_status()
        data = guilde.json()
        guild = data.get("guild", data)

        next_refresh = guild.get("nextChallengesRefresh")
        if next_refresh:
            ts = int(next_refresh)
            if ts > 1e10:
                ts = ts / 1000
            return datetime.fromtimestamp(ts).date()
    except Exception as e:
        print(f"Erreur récupération TB : {e}")
    return None

def is_gac_active():
    aujourd_hui = date.today()
    try:
        events = get_events()
        for e in events:
            if e.get('nameKey', '').startswith('SEASON_') and 'EVENT_NAME' in e.get('nameKey', ''):
                for inst in e.get('instance', []):
                    start = inst.get('startTime', 0)
                    end = inst.get('endTime', 0)
                    if start and end:
                        start_dt = datetime.fromtimestamp(int(start)/1000 if int(start) > 1e10 else int(start)).date()
                        end_dt = datetime.fromtimestamp(int(end)/1000 if int(end) > 1e10 else int(end)).date()
                        if start_dt <= aujourd_hui <= end_dt:
                            return True
        return False
    except Exception as e:
        print(f"Erreur API events: {e}")
        return False

def check_events():
    aujourd_hui = date.today()
    jour = aujourd_hui.day
    dernier_jour = dernier_jour_mois()
    messages = []
    
    #vaisseaux amiraux
    if jour == 15:
        messages.append("**Event Executor <@&1436064696456446002>**")
    if jour == 20:
        messages.append("**Event Leviathan**")
    if aujourd_hui.weekday() == 1 and is_gac_active():
        messages.append("**Inscription GA**")
    if jour == dernier_jour:
        messages.append("**Event Profundity <@&1436064696456446002>**")
    #TB
    next_tb = get_next_tb_date()
    if next_tb and next_tb == aujourd_hui + timedelta(days=1):
        messages.append("TB <@&1436064696456446002>")

    #Envoie final
    for message in messages:
        requests.post(DISCORD_WEBHOOK, json={"content": message})
        print(f"Message envoyé : {message[:40]}...")

if __name__ == "__main__":
    print(f"ALLY_CODE: '{ALLY_CODE}' type: {type(ALLY_CODE)}")
    print(f"=== Events checker {date.today()} ===")
    check_events()
