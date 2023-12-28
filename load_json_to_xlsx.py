# load_json_to_xlsx.py
"""
Takes raw_monsters.json file created by load_raw_to_json.py
and writes it out to an xlsx file in the format used by the fight_sheet.xlsx
"""
import json
import openpyxl

# === Helpers
HEADERS = [
    'Name', 'Type', 'Alignment', 'AC', 'AC type', 'HP', 'HP Formula', 'Speed',
    'Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha', 'Save Throws', 'Skills',
    'Damage Resistances', 'Damage Immunities', 'Condition Immunities',
    'Senses', 'Languages', 'Challenge', 'XP', 'Additional Settings',
    'Description', 'Actions', 'Legendary Actions'
]

SCHEMA = {
    1: 'name', 2: 'type', 3: 'alignment', 4: 'EXCEPTION', 5: 'EXCEPTION', 6: 'hit_points',
    7: 'hit_points_roll', 8: 'EXCEPTION', 9: 'strength', 10: 'dexterity', 11: 'constitution', 12: 'intelligence',
    13: 'wisdom', 14: 'charisma', 15: 'EXCEPTION', 16: 'EXCEPTION',
    17: 'EXCEPTION', 18: 'EXCEPTION', 19: 'EXCEPTION',
    20: 'EXCEPTION', 21: 'languages', 22: 'challenge_rating', 23: 'xp',
    24: 'challenge_rating', 25: 'EXCEPTION', 26: 'EXCEPTION', 27: 'EXCEPTION'
}

EXCCEPTIONS = [4, 5, 8, 15, 16, 17, 18, 19, 20, 25, 26, 27] # Currently not used

def create_header_map(headers:list) -> dict:
    """
    Takes a list of already ordered header names for xlsx sheet and 
    returns a dict with column number as key, and header as value.
    """
    header_map = {}

    for i, header in enumerate(headers):
        key = i + 1
        header_map[key] = f"{header}"

    return header_map

HEADER_MAP = create_header_map(HEADERS)

# === Main execution
# load in json file
input_path = "./data/raw_monsters.json"
with open(input_path, "r") as input_json:
    data = json.load(input_json)

# rows to write to xlsx
monster_rows = []

for json_item in data:
    # Create skeleton row
    curr_monster = {}
    for i in range(1, len(HEADERS)+1):
        curr_monster[i] = "NULL"

    for k in SCHEMA:
        if SCHEMA[k] != 'EXCEPTION':
            curr_monster[k] = json_item[SCHEMA[k]]
    
    monster_rows.append(curr_monster)

# Create xlsx file
workbook = openpyxl.Workbook()

# Select default worksheet
sheet = workbook.active

# Set headers
sheet.append(HEADERS)

# Add monsters
for monster in monster_rows:
    try:
        sheet.append(monster)
    except Exception as e:
             print(f"An error has occurred: {e}")

# Save workbook to file and close
workbook.save("./output/monsters_from_raw.xlsx")
workbook.close()