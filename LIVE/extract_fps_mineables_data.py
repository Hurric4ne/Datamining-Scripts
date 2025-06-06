import os
import re
import json

# Specify the directory containing the files
dirname = os.path.dirname(__file__)
directory = os.path.join(dirname, "base_files/mining/fps_mineables")

# Initialize the list to store the parsed data
result = []

# Regular expressions
name_pattern = re.compile(r"<EntityClassDefinition\.(\w+)")
breakable_pieces_pattern = re.compile(r'numPiecesOverride="(\d+)"')

# Iterate through all files in the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    
    # Skip if not a file
    if not os.path.isfile(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

        # Extract the rock name
        name_match = name_pattern.search(content)
        rockName = name_match.group(1) if name_match else None

        # Extract the number of breakable pieces
        breakable_pieces_match = breakable_pieces_pattern.search(content)
        breakablePieces = int(breakable_pieces_match.group(1)) if breakable_pieces_match else "N/A"

        # Append the extracted information to the result list
        result.append({
            "Name": rockName,
            "Breakable Pieces": breakablePieces,
        })

# Save the result to a JSON file
output_filepath = os.path.join(dirname, "json_files/fps_mineables_data.json")


with open(output_filepath, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, indent=4)

print(f"JSON file created at: {output_filepath}")
