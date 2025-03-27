import os
import re
import json

# Specify the directory containing the files
dirname = os.path.dirname(__file__)
directory = os.path.join(dirname, "base_files/armor/heavy/core")

# Initialize the list to store the parsed data
result = []

# Regular expressions
name_pattern = re.compile(r"<EntityClassDefinition\.(\w+)")
capacity_pattern = ''
volume_pattern = re.compile(r"<inventoryOccupancyVolume.*?microSCU=\"(\d+)\"")
minTemp_pattern = re.compile(r'MinResistance="(-?\d+\.?\d*)"')
maxTemp_pattern = re.compile(r'MaxResistance="(-?\d+\.?\d*)"')

dmgResist_pattern = re.compile(r"<EntityClassDefinition\.(\w+)")

# Iterate through all files in the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    
    # Skip if not a file
    if not os.path.isfile(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

        # Extract the name
        name_match = name_pattern.search(content)
        name = name_match.group(1) if name_match else 'N/A'

        # Extract the volume
        volume_match = volume_pattern.search(content)
        volume = volume_match.group(1) if volume_match else "N/A"

        # Extract the capacity

        # Extract the minTemp and maxTemp
        minTemp_match = minTemp_pattern.search(content)
        minTemp = minTemp_match.group(1) if minTemp_match else "N/A"
        maxTemp_match = maxTemp_pattern.search(content)
        maxTemp = maxTemp_match.group(1) if maxTemp_match else "N/A"

        # Append the extracted information to the result list
        result.append({
            "Name": name,
            "Volume (mSCU)": volume,
            "Min Temp (C)": minTemp,
            "Max Temp (C)": maxTemp
        })

# Save the result to a JSON file
output_filepath = os.path.join(dirname, "json_files/armor_data.json")


with open(output_filepath, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, indent=4)

print(f"JSON file created at: {output_filepath}")
