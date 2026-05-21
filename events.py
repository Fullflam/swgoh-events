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
        messages.append("**Event Executor <@&1105957047826124841>**")

    if jour == 20:
        messages.append("**Event Leviathan <@&1133869314232029369>**")

    if aujourd_hui.weekday() == 1:
        messages.append("**Inscription GA <@419575551163105281>**")
         
    if jour == dernier_jour:
        messages.append("**Event Profundity <@&1105957094294835271>**")
    messages.append("test")
    for message in messages:
        requests.post(DISCORD_WEBHOOK, json={"content": message})
        print(f"Message envoyé : {message[:40]}...")

if __name__ == "__main__":
    print(f"=== Events checker {date.today()} ===")
    check_events()
