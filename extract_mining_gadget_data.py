import os
import re
import json

# Specify the directory containing the files
directory = "base_files/mining/gadgets"

# Initialize the list to store the parsed data
result = []

# Regular expressions
name_pattern = re.compile(r"<EntityClassDefinition\.(\w+)")
resistance_modifier_pattern = re.compile(r'<resistanceModifier [^>]*value="(-?\d+\.\d+)"')
instability_modifier_pattern = re.compile(r'<laserInstability [^>]*value="(-?\d+\.\d+)"')
charge_rate_pattern = re.compile(r'<optimalChargeWindowRateModifier [^>]*value="(-?\d+\.\d+)"')
charge_window_pattern = re.compile(r'<optimalChargeWindowSizeModifier [^>]*value="(-?\d+\.\d+)"')
overcharge_rate_pattern = re.compile(r'<catastrophicChargeWindowRateModifier [^>]*value="(-?\d+\.\d+)"')
cluster_modifier_pattern = re.compile(r'<clusterFactorModifier [^>]*value="(-?\d+\.\d+)"')
shatter_damage_pattern = re.compile(r'<shatterdamageModifier [^>]*value="(-?\d+\.\d+)"')

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
        name = name_match.group(1) if name_match else None

        # Extract the window-size modifier
        charge_window = charge_window_pattern.search(content)
        chargeWindowModifier = float(charge_window.group(1)) if charge_window else "N/A"

        # Extract the charge-rate modifier
        charge_rate = charge_rate_pattern.search(content)
        chargeRateModifier = float(charge_rate.group(1)) if charge_rate else "N/A"

        # Extract the instability modifier
        instability_modifier = instability_modifier_pattern.search(content)
        instabilityModifier = float(instability_modifier.group(1)) if instability_modifier else "N/A"

        # Extract the resistance modifier
        resistance_modifier = resistance_modifier_pattern.search(content)
        resistanceModifier = float(resistance_modifier.group(1)) if resistance_modifier else "N/A"

        # Extract the cluster modifier
        cluster_modifier = cluster_modifier_pattern.search(content)
        clusterModifier = float(cluster_modifier.group(1)) if cluster_modifier else "N/A"

        # Extract the shatter damage modifier
        shatter_damage = shatter_damage_pattern.search(content)
        shatterDamageModifier = float(shatter_damage.group(1)) if shatter_damage else "N/A"

        # Extract the overcharge-rate modifier
        overcharge_rate = overcharge_rate_pattern.search(content)
        overchargeRateModifier = float(overcharge_rate.group(1)) if overcharge_rate else "N/A"

        # Append the extracted information to the result list
        result.append({
            "Name": name,
            "Optimal Charge Window Size (%)": chargeWindowModifier,
            "Optimal Charge Window Rate (%)": chargeRateModifier,
            "Laser Instability (%)": instabilityModifier,
            "Resistance (%)": resistanceModifier,
            "Cluster Modifier (%)": clusterModifier,
            "Shatter Damage (%)": shatterDamageModifier,
            "Catastrophic Charge Rate (%)": overchargeRateModifier,
        })

# Save the result to a JSON file
output_filepath = "json_files/mining_gadgets_data.json"


with open(output_filepath, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, indent=4)

print(f"JSON file created at: {output_filepath}")
