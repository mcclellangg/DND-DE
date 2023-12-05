# load_raw_to_json.py
"""
Takes SRD file as input and parses values based on rules into json file. 

raw data layer
- basic row count validation
- extract desired data fields from SRD file, but don't alter them yet
"""
import json

# === Helpers
def get_named_values(item: dict, curr_monster: dict) -> dict:
    """
    Takes an item from json data, curr_monster (dict) and adds in all fields that can be keyed into
    without exceptions.
    """
    updated_monster = curr_monster

    # Try item[column] for value in named
    NAMED_VALUES = [
    "index"
    ,"name"
    ,"type"
    ,"speed"
    ,"alignment"
    ,"hit_points"
    ,"hit_points_roll"
    ,"strength"
    ,"dexterity"
    ,"constitution"
    ,"intelligence"
    ,"wisdom"
    ,"charisma"
    ,"size"
    ,"damage_resistances"
    ,"damage_immunities"
    ,"damage_vulnerabilities"
    ,"senses"
    ,"languages" # string of comma seperated values
    ,"challenge_rating"
    ,"xp"
    ]
    for key in NAMED_VALUES:
        updated_monster[key] = item[key]
    
    return updated_monster

def get_item_speed(item: dict, curr_monster: dict) -> dict:
    """
    Update monster dict w/ speed values
    """
    updated_speed_monster = curr_monster
    
    try:
        speed_dict = item["speed"]
        if "hover" in speed_dict:
            speed_dict["hover"] = "true"
    except Exception as e:
       print(f"Error: {e}")
    
    updated_speed_monster["speed"] = speed_dict

    return updated_speed_monster

def get_monster_ac(item: dict, curr_monster: dict) -> dict:
    """
    Update monster armor class w/ value, type & armor name if dict contains armor

    ASSUMPTION: len (item["armor_class"]) not expected to exceed 1 or be 0
    """
    updated_ac_monster = curr_monster
    updated_ac_monster["armor_class"] = {}

    if len(item["armor_class"]) > 1:
        # ERROR
        print(f"{item['index']} armor_class exceeds expected length")
        # BUG: handle error for exceptions
    
    updated_ac_monster["armor_class"]["type"] = item["armor_class"][0]["type"]
    updated_ac_monster["armor_class"]["value"] = item["armor_class"][0]["value"]

    # ASSUMPTION: item["armor_class"][0]["armor"] always == 1
    if "armor" in item["armor_class"][0]:
        updated_ac_monster["armor_class"]["armor_name"] = item["armor_class"][0]["armor"][0]["name"]
    
    return updated_ac_monster

def get_proficiencies(item: dict) -> list:
    """
    item["proficiencies"] is a list of dictionaries containing saving throws, and/or skills. This function return a list of dicts in the following format:
    { "value" : int
      ,"proficiency_name" : str
    }
    """
    proficiencies = []
    for p in item["proficiencies"]:
        d = {}
        d["proficiency_name"] = p["proficiency"]["name"]
        d["value"] = p["value"] # value is int
        
        # ASSUMPTION: proficiencies must be skill or saving_throw
        if 'Skill' in p["proficiency"]["name"]:
            d["type"] = "skill"
        
        elif "Saving Throw" in p["proficiency"]["name"]:
            d["type"] = "saving_throw"
        
        else:
            d["type"] = "NULL"

        proficiencies.append(d)
    
    return proficiencies

def get_actions_name_and_desc(item: dict, action_type="actions") -> list:
    """
    item["actions"] is a list of dicts. Parses each action for it's name and desc
    action_type can be "legendary_actions" or "actions"
    item must have "actions" field, but may not have "legendary_actions".
    """
    actions = []
    for a in item[action_type]:
        d = {}
        d["name"] = a["name"]
        d["desc"] = a["desc"]
        actions.append(d)
    
    return actions


# === Execute script
input_path = "./data/5e-SRD-Monsters.json"
output_path = "./data/raw_monsters.json"
raw_monsters = []

# Generate json data
with open(input_path, "r") as input_json:
    data = json.load(input_json)

# Iterate and extract
for item in data:
    # Create monster and add to raw
    # curr_monster={} is redundant and unesscessary ...
    raw_monster = {}
    
    # Update with base values (items in srd where value can be accessed by key, and has no exceptions)
    base_values = get_named_values(item=item, curr_monster={})
    raw_monster.update(base_values)

    # Get ac
    armor_class = get_monster_ac(item=item, curr_monster={})
    raw_monster.update(armor_class)
    
    # Get proficiencies
    proficiencies = get_proficiencies(item=item)
    raw_monster["proficiencies"] = proficiencies

    # Special_abilities (optional field)
    if "special_abilities" in item:
        raw_monster["special_abilities"] = item["special_abilities"]
    
    # Get actions
    if "actions" in item:
        actions = get_actions_name_and_desc(item=item)
        raw_monster["actions"] = actions

    if "legendary_actions" in item:
        legendary_acts = get_actions_name_and_desc(item=item, action_type="legendary_actions")
        raw_monster["legendary_actions"] = legendary_acts

    # TODO: perform some validation on it before considering updated
    updated_raw_monster = raw_monster
    
    # Add final updated row
    raw_monsters.append(updated_raw_monster)

# Write to output
with open(output_path, "w") as output:
    json.dump(raw_monsters, output)
