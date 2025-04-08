import re
import json
import os

# Specify the directory containing the files
dirname = os.path.dirname(__file__)
localization_file = os.path.join(dirname, "base_files/global_utf8.ini")

# Define the regex pattern
pattern = r'["\'](\w+(?: \w+)?)["\']'

# Read the file and store lines in a dictionary
data = {}
with open(localization_file, "r", encoding="utf-8") as file:
    for line in file:
        if "=" in line:
            key, value = line.strip().split("=", 1)  # Split at the first '='
            data[key] = value

# Extract matching entries where the key contains "item"
matching_entries = {
    key: value for key, value in data.items() 
    if "item_Name" in key and re.search(pattern, value)
}

# Sort the matching entries based on the words within the quotes (alphabetically)
sorted_entries = {key: value for key, value in sorted(matching_entries.items(), key=lambda item: re.search(pattern, item[1]).group(1).lower())}

# Save the result to a JSON file
output_filepath = os.path.join(dirname, "json_files/quoted_items.json")
with open(output_filepath, "w", encoding="utf-8") as json_file:
    json.dump(sorted_entries, json_file, indent=4, ensure_ascii=False)

print(f"Matching entries saved to {output_filepath}")
