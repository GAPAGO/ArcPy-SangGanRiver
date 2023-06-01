import csv
import os
from collections import defaultdict

# Set the input folder path
input_folder = r"D:\ShenZeyu20230308\ArcPy_SangGanHe\attribute table"
# Set the output folder path
output_folder = r"D:\ShenZeyu20230308\ArcPy_SangGanHe\merged table"

# Iterate through the files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        # Set the input file path
        input_file = os.path.join(input_folder, filename)

        # Create a dictionary to store the summed Shape_Area values
        sum_dict = defaultdict(float)

        # Create a dictionary to store the unique Area values
        area_dict = {}

        # Open the input file
        with open(input_file, "r") as f:
            # Create a CSV reader
            reader = csv.DictReader(f)

            # Iterate through the rows in the CSV file
            for row in reader:
                # Get the Cell_Index and Assigned_c values
                cell_index = row["Cell_Index"]
                assigned_c = row["Assigned_c"]

                # Use a tuple of Cell_Index and Assigned_c as the key and add the Shape_Area value to the sum
                sum_dict[(cell_index, assigned_c)] += float(row["Shape_Area"])

                # Store the unique Area value
                area_dict[(cell_index, assigned_c)] = row["Area"]

        # Set the output file path
        output_file = os.path.join(output_folder, filename)

        # Open the output file
        with open(output_file, "w", newline="") as f:
            # Create a CSV writer
            writer = csv.writer(f)

            # Write the header row
            writer.writerow(["Cell_Index", "Assigned_c", "Sum of Shape_Area", "Area"])

            # Write the data rows
            for key, value in sum_dict.items():
                writer.writerow([key[0], key[1], value, area_dict[key]])
