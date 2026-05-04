from collections import defaultdict

from typing import Literal
import requests
import json

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
char_ids = [
"10000002",
"10000003",
"10000006",
"10000014",
"10000015",
"10000016",
"10000020",
"10000021",
"10000022",
"10000023",
"10000024",
"10000025",
"10000026",
"10000027",
"10000029",
"10000030",
"10000031",
"10000032",
"10000033",
"10000034",
"10000035",
"10000036",
"10000037",
"10000038",
"10000039",
"10000041",
"10000042",
"10000043",
"10000044",
"10000045",
"10000046",
"10000047",
"10000048",
"10000049",
"10000050",
"10000051",
"10000052",
"10000053",
"10000054",
"10000055",
"10000056",
"10000057",
"10000058",
"10000059",
"10000060",
"10000061",
"10000062",
"10000063",
"10000064",
"10000065",
"10000066",
"10000067",
"10000068",
"10000069",
"10000070",
"10000071",
"10000072",
"10000073",
"10000074",
"10000075",
"10000076",
"10000077",
"10000078",
"10000079",
"10000080",
"10000081",
"10000082",
"10000083",
"10000084",
"10000085",
"10000086",
"10000087",
"10000088",
"10000089",
"10000090",
"10000091",
"10000092",
"10000093",
"10000094",
"10000095",
"10000096",
"10000097",
"10000098",
"10000099",
"10000100",
"10000101",
"10000102",
"10000103",
"10000104",
"10000105",
"10000106",
"10000107",
"10000108",
"10000109",
"10000110",
"10000111",
"10000112",
"10000113",
"10000114",
"10000115",
"10000116",
"10000119",
"10000120",
"10000121",
"10000122",
"10000123",
"10000124",
"10000125",
"10000126",
"10000127",
"10000128",
"10000129",
"10000130",
"10000131",
"10000132",
"10000005_ANEMO",
"10000005_DENDRO",
"10000005_ELECTRO",
"10000005_GEO",
"10000005_HYDRO",
"10000005_PYRO"]

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
