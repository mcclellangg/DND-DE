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

def get_proficiencies_for_xlsx(prof_type:str, profs: list) -> str:
    """
    Takes proficiences from json data (list of dictionaries) and returns a parsed string
    to be written to xlsx column based on prof_type provided (saving_throw or skill)
    """
    prof_type_flags = {
        "saving_throw": "Saving"
        ,"skill" : "Skill"
    }

    strip_values = {
        "saving_throw": 14 # len("Saving Throw: ")
        ,"skill" : 7 # len( "Skill: ")
    }

    prof_flag = prof_type_flags[prof_type]
    
    # Create dict of values based on flag
    profs_d = {}
    for d in profs:
        curr_name = d["proficiency_name"]
        curr_value = d["value"]
        # ASSUMPTION: "proficiency_name" always begins with "Saving Throw: " or "Skill: "
        parsed_name = curr_name[strip_values[prof_type]:]

        if prof_flag in curr_name:
            profs_d[parsed_name] = curr_value 
    
    # Parse dict
    if len(profs_d) > 0:
        parsed_profs = ', '.join(key + " +" + str(val) for key, val in profs_d.items())
    else:
        parsed_profs = f"No {prof_type} for this creatrue."
    
    return parsed_profs

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
        # AC (value)
        elif k == 4:
            try:
                curr_monster[k] = json_item["armor_class"]["value"]
            except Exception as e:
                print(f"An error has occurred: {e}")
        # AC_type
        elif k == 5:
            try:
                curr_monster[k] = json_item["armor_class"]["type"]
            except Exception as e:
                print(f"An error has occurred: {e}")
        # Speed
        elif k == 8:
            try:
                speed_dict = json_item["speed"]
                if "hover" in speed_dict:
                    speed_dict["hover"] = "true"
                parsed_speed = ','.join(key + " " + val for key, val in speed_dict.items())
                curr_monster[k] = (parsed_speed)
            except Exception as e:
                print(f"Monster speed is an exception and will be written as NULL")
                print(f"Index of monster with exception: {json_item['index']}")
        # Saving throws
        elif k == 15:
            try:
                curr_monster[k] = get_proficiencies_for_xlsx(prof_type="saving_throw",profs=json_item["proficiencies"] )
            except Exception as e:
                print(f"An error has occurred: {e}")
        # Skills
        elif k == 16:
            try:
                curr_monster[k] = get_proficiencies_for_xlsx(prof_type="skill",profs=json_item["proficiencies"] )
            except Exception as e:
                print(f"An error has occurred: {e}")
        
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