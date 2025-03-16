import os
import re
import json

# Specify the directory containing the files
directory = "ptu_tests/base_files/mining/lasers"

# Initialize the list to store the parsed data
result = []

# Regular expressions
name_pattern = re.compile(r"<EntityClassDefinition\.(\w+)")
optimal_range_pattern = re.compile(r'fullDamageRange="(\d+\.\d+)"')
maximum_range_pattern = re.compile(r'zeroDamageRange="(\d+\.\d+)"')
minimum_throttle_pattern = re.compile(r'throttleMinimum="(\d+\.\d+)"')
power_pattern = re.compile(r'DamageEnergy="(\d+\.\d+)"')
filter_modifier_pattern = re.compile(r'<filterModifier [^>]*value="(-?\d+\.\d+)"')
laser_instability_pattern = re.compile(r'<laserInstability [^>]*value="(-?\d+\.\d+)"')
optimal_charge_window_pattern = re.compile(r'<optimalChargeWindowSizeModifier [^>]*value="(-?\d+\.\d+)"')
optimal_charge_rate_pattern = re.compile(r'<optimalChargeWindowRateModifier [^>]*value="(-?\d+\.\d+)"')
resistance_modifier_pattern = re.compile(r'<resistanceModifier [^>]*value="(-?\d+\.\d+)"')
module_slot_pattern = re.compile(r'DisplayName="Sub_Item_Slot"')
size_pattern = re.compile(r'\sSize="(\d+)"')

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

        # Extract the optimal range
        optimal_range = optimal_range_pattern.search(content)
        optimalRange = float(optimal_range.group(1))
        # Extract the maximum range
        maximum_range = maximum_range_pattern.search(content)
        maxRange = float(maximum_range.group(1))

        # Extract the minimum throttle
        minimum_throttle = minimum_throttle_pattern.search(content)
        minThrottle = float(minimum_throttle.group(1)) * 100

        # Extract the maximum power + extraction power
        power_matches = power_pattern.findall(content)
        maxPower = float(power_matches[0])
        extractPower = float(power_matches[1]) if len(power_matches) > 1 else "N/A"

        # Calculate the minimum power
        minPower = (maxPower * minThrottle) / 100

        # Extract the filter modifier
        filter_modifier = filter_modifier_pattern.search(content)
        filterModifier = float(filter_modifier.group(1)) if filter_modifier else "N/A"

        # Extract the laser instability
        laser_instability = laser_instability_pattern.search(content)
        laserInstability = float(laser_instability.group(1)) if laser_instability else "N/A"

        # Extract the optimal window size
        optimal_charge_window = optimal_charge_window_pattern.search(content)
        optimalChargeWindow = float(optimal_charge_window.group(1)) if optimal_charge_window else "N/A"

        # Extract the optimal charge rate
        optimal_charge_rate = optimal_charge_rate_pattern.search(content)
        optimalChargeRate = float(optimal_charge_rate.group(1)) if optimal_charge_rate else "N/A"

        # Extract the resistance modifier
        resistance_modifier = resistance_modifier_pattern.search(content)
        resistanceModifier = float(resistance_modifier.group(1)) if resistance_modifier else "N/A"

        # Extract the module slot amount
        module_slot = module_slot_pattern.findall(content)
        moduleSlots = len(module_slot) if module_slot else "N/A"

        # Extract the size
        size = size_pattern.search(content)
        itemSize = int(size.group(1)) if size else "N/A"

        # Append the extracted information to the result list
        result.append({
            "Name": name,
            "Size": itemSize,
            "Optimal Range (m)": optimalRange,
            "Maximum Range (m)": maxRange,
            "Minumum Laser Power": minPower,
            "Maximum Laser Power": maxPower,
            "Extraction Laser Power": extractPower,
            "Module Slots": moduleSlots,
            "Laser Instability (%)": laserInstability,
            "Optimal Charge Window Rate (%)": optimalChargeRate,
            "Inert Material Level (%)": filterModifier,
            "Optimal Charge Window Size (%)": optimalChargeWindow,
            "Resistance (%)": resistanceModifier,
            "Throttle min (%)": minThrottle,
        })

# Save the result to a JSON file
output_filepath = "ptu_tests/json_files/mining_laser_data.json"


with open(output_filepath, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, indent=4)

print(f"JSON file created at: {output_filepath}")
