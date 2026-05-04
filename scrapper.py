from collections import defaultdict

from typing import Literal
import requests
import json

from env import char_ids

import re
import os

directories = ["characters", "weapons"]
for directory in directories:
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory}'.")   

html_cleaner = re.compile('<.*?>') 

# Senin istediğin tam liste stat eşleşmeleri
STAT_REPLACE = {
    "Max HP": "HP",
    "Elemental Mastery": "EM",
    "Attack": "ATK",
    "Defense": "DEF",
    "Base ATK": "BaseATK",
    "Attack%": "ATK%",
    "HP%": "HP%",
    "Defense%": "DEF%",
    "Crit RATE": "CritRate%",
    "Crit DMG": "CritDMG%",
    "Energy Recharge": "ER%",
    "Physical DMG Bonus": "PhysicalDMG%",
    "Anemo DMG Bonus": "AnemoDMG%",
    "Geo DMG Bonus": "GeoDMG%",
    "Electro DMG Bonus": "ElectroDMG%",
    "Dendro DMG Bonus": "DendroDMG%",
    "Hydro DMG Bonus": "HydroDMG%",
    "Pyro DMG Bonus": "PyroDMG%",
    "Cryo DMG Bonus": "CryoDMG%",
}


def fix_stat_name(name):
    return STAT_REPLACE.get(name, name.replace(" ", ""))

def fetch_character(char_id):
    url = f"https://api.lunaris.moe/data/6.5.54.2/en/char/{char_id}.json"
    r = requests.get(url)
    if r.status_code != 200: return None
    
    d = r.json()
    
    # Mapping Lunaris internal keys to your desired Talent structure
    raw_skills = d.get("skills", {})

    talents = {
        "normal_attack": {
            "name": raw_skills["normalattack"].get("name"), 
            "multipliers": raw_skills["normalattack"].get("multipliers"),
            "description": html_cleaner.sub('', raw_skills["normalattack"].get("description"))},
        "elemental_skill": {
            "name": raw_skills["elementalskill"].get("name"), 
            "multipliers": raw_skills["elementalskill"].get("multipliers"),
            "description": html_cleaner.sub('', raw_skills["elementalskill"].get("description"))},
        "elemental_burst": {
            "name": raw_skills["elementalburst"].get("name"), 
            "multipliers": raw_skills["elementalburst"].get("multipliers"),
            "description": html_cleaner.sub('', raw_skills["elementalburst"].get("description"))}
    }

    base_stats = {}
    
    l1 = d["info"]["attributes"][0]
    base_stats["base_hp"] = l1.get("hp")
    base_stats["base_atk"] = l1.get("atk")
    base_stats["base_def"] = l1.get("def")

    l90 = d["info"]["attributes"][91]
    base_stats["max_lvl_hp"] = l90.get("hp")
    base_stats["max_lvl_atk"] = l90.get("atk")
    base_stats["max_lvl_def"] = l90.get("def")
    POSSIBLE_ASCENSION_STATS = set(["CRIT Rate%", "CRIT DMG%", "ER", "EM", "Anemo%", "Geo%", "Electro%", "Dendro%", "Hydro%", "Pyro%", "Cryo%", "ATK%", "HP%", "DEF%"])
    for stat in POSSIBLE_ASCENSION_STATS:
        if l90.get(stat) is None: continue
        base_stats[stat] = l90.get(stat)


    return {
        "name": d["info"]["name"],
        "weapon": d["info"]["weapon"],
        "rarity": d["info"].get("rarity"),
        "element": d["info"].get("element"),
        "base_stats": base_stats,
        "talents": talents
    }

# Execution logic remains similar

def fetch_weapon(weap_id):
    url = f"https://api.lunaris.moe/data/6.5.54.2/en/weapon/{weap_id}.json"
    r = requests.get(url)
    if r.status_code != 200: return None
    
    d = r.json()
    
    # Silah statları (BaseATK vb.)
    stats_fixed = {}
    for lvl, s_dict in d.get("stats", {}).items():
        stats_fixed[lvl] = {fix_stat_name(k): v for k, v in s_dict.items()}

    return {
        "name": d.get("name"),
        "type": d.get("weaponType"),
        "quality": d.get("qualityType"),
        "desc": d.get("weaponDesc"),
        "refinements": d.get("refinements"),
        "stats": stats_fixed
    }

# --- ÇALIŞTIRMA BÖLÜMÜ ---

# Senin verdiğin listeden örnek ID'ler
weap_ids = ["11101", "15515"]

db = {"characters": [], "weapons": []}

for cid in char_ids:
    print(f"Karakter çekiliyor: {cid}")
    res = fetch_character(cid)
    with open(f'characters/{res["name"].replace(" ", "_")}.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    if res: db["characters"].append(res)

for wid in weap_ids:
    print(f"Silah çekiliyor: {wid}")
    res = fetch_weapon(wid)
    with open(f'weapons/{res["name"].replace(" ", "_")}.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    if res: db["weapons"].append(res)

with open('genshin_db.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=4, ensure_ascii=False)

print("Tamamlandı! genshin_db.json dosyasını kontrol et.")
