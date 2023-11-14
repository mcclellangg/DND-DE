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
HEADERS = ["index", "name", "size", "challenge_rating", "hit_points", "speed", "armor_class"]

walk_speed_exceptions = ["air-elemental", "giant-shark", "hunter-shark", "killer-whale", "quipper", "reef-shark", "sea-horse", "vampire-mist"]

# ==== TODO ===
# exception_fields = {
    # "speed" : "TODO" #Add keys for swim
    # ,"armor_clss" : "TODO"
# }
# === TODO ===

# === Functions
def validate_row_length(row, HEADERS):
    """This function validates that the row_to_write will have the same number of columns as the HEADERS"""
    if len(row) != len(HEADERS):
        logging.error(f"Row length {len(row)} != HEADER length {len(HEADERS)}")
        logging.error(f"Row in error {row}")
        return False
    else:
        return True

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
    #BUG: ensure when writing row, that len == HEADERS
    row_to_write = []

    # Populate row_to_write
    for column in HEADERS:
        if column == "speed":
            if item["index"] not in walk_speed_exceptions:
                row_to_write.append(item[column]["walk"])
            else:
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
workbook.save("./output/monsters.xlsx")
workbook.close()