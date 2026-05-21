import requests
import os
from datetime import datetime, date
from calendar import monthrange

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")

def dernier_jour_mois():
    aujourd_hui = date.today()
    return monthrange(aujourd_hui.year, aujourd_hui.month)[1]

def check_events():
    aujourd_hui = date.today()
    jour = aujourd_hui.day
    dernier_jour = dernier_jour_mois()
    mois = aujourd_hui.strftime("%B %Y")

    messages = []

    if jour == 15:
        messages.append("# Executor disponible aujourd'hui !\n> L'event Executor est actif — foncez !")

    if jour == 20:
        messages.append("# Leviathan disponible aujourd'hui !\n> L'event Leviathan est actif — foncez !")

    if jour == dernier_jour:
        messages.append("# Profondeur disponible aujourd'hui !\n> L'event Profondeur est actif — dernier jour du mois !")

    for message in messages:
        requests.post(DISCORD_WEBHOOK, json={"content": message})
        print(f"Message envoyé : {message[:40]}...")

if __name__ == "__main__":
    print(f"=== Events checker {date.today()} ===")
    check_events()
