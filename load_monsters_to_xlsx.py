# load_monsters_to_xlsx
"""
This function will read the data from the 5e-SRD-Monsters.json and write it into a xlsx file.
"""

import openpyxl
import json
import logging

# Configure logger
# TODO: Save/create log file function
logging.basicConfig(filename='.\\logs\\app.log', level=logging.DEBUG)

# === Constants & variables
# BUG:HEADERS assumes input column maps exactly to output column (Cases exist where this is not true, and will need to be solved for) 
HEADERS = ["index"
           ,"name"
           ,"type"
           ,"alignment"
           ,"armor_class"
           ,"hit_points"
           ,"hit_points_roll"
           ,"speed"
           ,"strength"
           ,"dexterity"
           ,"constitution"
           ,"intelligence"
           ,"wisdom"
           ,"charisma"
           ,"size"
           ,"languages"
           ,"challenge_rating"
           ,"xp"
           ,"save_throws"
           ,"skills"
           ,"damage_resistances"
           ,"damage_immunities"
           ,"condition_immunities"
           ,"senses"
           ,"special_abilities"
           ,"actions"
           ,"legendary_actions"]

# === Functions
def validate_row_length(row, HEADERS):
    """This function validates that the row_to_write will have the same number of columns as the HEADERS"""
    if len(row) != len(HEADERS):
        logging.error(f"Row length {len(row)} != HEADER length {len(HEADERS)}")
        logging.error(f"Row in error {row}")
        return False
    else:
        return True

def create_saves_dict(profs:list) -> dict:
    """Takes a list of proficiencies, searches for save_throws and returns a dict of saving throw names & values"""
    # item["proficiencies"]
    save_throws_d = {}
    for d in profs:
        curr_name = d["proficiency"]["name"]
        curr_value = d["value"]
        if "Saving Throw" in curr_name:
            save_throws_d[curr_name] = curr_value
    return save_throws_d

def create_skills_dict(profs:list) -> dict:
    skills_d = {}
    for d in profs:
        curr_name = d["proficiency"]["name"]
        curr_value = d["value"]
        if "Skill" in curr_name:
            skills_d[curr_name] = curr_value
    return skills_d

# === EXECUTE ===

# Create new workbook
workbook = openpyxl.Workbook()

# Select default worksheet
sheet = workbook.active

# Set headers
sheet.append(HEADERS)

# Read in json data
input_json_file = "./DATA/5e-SRD-Monsters.json"

# Read the JSON data from the input file
with open(input_json_file, "r") as json_file:
    data = json.load(json_file)

# Write json data to output
for item in data:
    row_to_write = []

    # Populate row_to_write
    for column in HEADERS:
        if column == "speed":
            try:
                speed_dict = item["speed"]
                if "hover" in speed_dict:
                    speed_dict["hover"] = "true"
                parsed_speed = ','.join(key + " " + val for key, val in speed_dict.items())
                row_to_write.append(parsed_speed)
            except Exception as e:
                row_to_write.append("NULL")
                logging.info(f"Monster speed is an exception and will be written as NULL")
                logging.info(f"Index of monster with exception: {item['index']}")
        
        elif column == "armor_class":
            try:
                row_to_write.append(item[column][0]["value"])
            #BUG: does not catch exceptions
            except Exception as e:
                logging.info(f"Monster armor_class is an exception and will not be written to output xlsx")
                logging.info(f"Index of monster with exception: {item['index']}")
        
        elif column == "save_throws":
            save_throws_d = create_saves_dict(item["proficiencies"])
            if len(save_throws_d) > 0:
                parsed_saves = ','.join(key + " : " + str(val) for key, val in save_throws_d.items())
                row_to_write.append(parsed_saves)
            else:
                row_to_write.append("NULL")
                logging.info(f"Monster has no save_throw proficiencies")
                logging.info(f"Index of monster with save_throw exception: {item['index']}")
        
        elif column == "skills":
            skills_d = create_skills_dict(item["proficiencies"])
            if len(skills_d) > 0:
                parsed_saves = ','.join(key + " : " + str(val) for key, val in skills_d.items())
                row_to_write.append(parsed_saves)
            else:
                row_to_write.append("NULL")
                logging.info(f"Monster has no skill proficiencies")
                logging.info(f"Index of monster with skill proficiency exception: {item['index']}")
        
        elif column == "damage_resistances" or column == "damage_immunities":
            # Concat into single string
            dmg_item_l = item[column]
            if len(dmg_item_l) > 0:
                dmg_item_s = ""
                for s in dmg_item_l:
                    dmg_item_s += s + ', ' # HACK
                row_to_write.append(dmg_item_s)
            else:
                row_to_write.append("NULL")
                logging.info(f"Index: {item['index']} has no {column} values")
        
        elif column == "condition_immunities":
            immunities_d = item["condition_immunities"]
            # Retrieve only names
            if immunities_d:
                condition_names = [d["name"] for d in immunities_d] # unclear variable
                row_to_write.append(str(condition_names)) # HACK
            else:
                row_to_write.append("NULL")
                logging.info(f"Index: {item['index']} has no {column} values")
        
        elif column == "senses":
            # item["senses"] returns a dict
            senses_dict = item["senses"]
            parsed_senses = ','.join(key + " : " + str(val) for key, val in senses_dict.items())
            row_to_write.append(parsed_senses)
        
        elif column == "special_abilities":
            # item["special_abilities"] returns list of dicts
            try:
                item["special_abilities"]
                abilities_list = [d["name"] + ". " + d["desc"] for d in item["special_abilities"]]
                # ASSUMPTION: list is never null/empty
                abilities_string = " ".join(abilities_list)
                row_to_write.append(abilities_string)
            except Exception as e:
                # HACK: grab KeyError specifically not just general exceptions
                logging.warning(f"Likely a key error occured for {item['index']} due to special_abilities")
                row_to_write.append("NULL")
        
        elif column == "actions":
            # item["actions"] returns list of dicts
            try:
                item["actions"]
                actions_list = [d["name"] + ". " + d["desc"] for d in item["actions"]]
                actions_string = " ".join(actions_list)
                row_to_write.append(actions_string)
            except Exception as e:
                logging.warning(f"Following occured for {item['index']} due to actions: {e}")
                row_to_write.append("NULL")
        
        elif column == "legendary_actions":
            if "legendary_actions" in item:
                leg_actions_list = [d["name"] + ". " + d["desc"] for d in item["legendary_actions"]]
                leg_actions_string = " ".join(leg_actions_list)
                row_to_write.append(leg_actions_string)
            else:
                logging.info(f"No legendary_actions for item_index: {item['index']}")
                row_to_write.append("NULL")

        else:
            try:
                row_to_write.append(item[column])
            except Exception as e:
                print(f"While trying to write value: {item[column]} of item: {item} to column: {column} the following error has occurred: {e}")
    
    # Write row to sheet
    if validate_row_length(row_to_write, HEADERS):
        try:
            sheet.append(row_to_write)
        except Exception as e:
             print(f"An error has occurred: {e}")
    else:
        logging.info("Terminating due to row validation error")
        break

# Save workbook to file and close
workbook.save("./output/leg_actions_test.xlsx")
workbook.close()