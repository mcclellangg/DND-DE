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
        print(f"Exiting program")
        # TODO: return, break or exit
        exit
    
    updated_ac_monster["armor_class"]["type"] = item["armor_class"][0]["type"]
    updated_ac_monster["armor_class"]["value"] = item["armor_class"][0]["value"]

    # ASSUMPTION: item["armor_class"][0]["armor"] always == 1
    if "armor" in item["armor_class"][0]:
        updated_ac_monster["armor_class"]["armor_name"] = item["armor_class"][0]["armor"][0]["name"]
    
    return updated_ac_monster

# === Execute script
input_path = "./data/5e-SRD-Monsters.json"
output_path = "./data/raw_monsters.json"
raw_monsters = []

with open(input_path, "r") as input_json:
    data = json.load(input_json)

for item in data:
    # Create monster and add to raw
    # curr_monster={} is redundant and unesscessary ...
    raw_monster = {}
    
    # Update with base values (items in srd where value can be accessed by key, and has no exceptions)
    base_values = get_named_values(item=item, curr_monster={})
    raw_monster.update(base_values)

    # Get speed
    speed = get_item_speed(item=item, curr_monster={})
    raw_monster.update(speed)

    # Get ac
    armor_class = get_monster_ac(item=item, curr_monster={})
    raw_monster.update(armor_class)
    
    # TODO: perform some validation on it before considering updated
    # BUG: currently load_raw process is only loading 333 monsters out of 335
    updated_raw_monster = raw_monster
    
    # Add final updated row
    raw_monsters.append(updated_raw_monster)

# Write to output
with open(output_path, "w") as output:
    json.dump(raw_monsters, output)
