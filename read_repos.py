import pandas as pd
import subprocess

# Path to the Excel file
excel_filename = "image_data.xlsx"  # Update the filename if needed

# Read the Excel file
df = pd.read_excel(excel_filename)

# Loop through rows using iterrows()
for index, row in df.iterrows():
    repository_name = row["Image"]  # Assuming "Repository Name" is the column name
    print(repository_name)


# Build the command
command = ["docker", "pull", repository_name]

# Run the command
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True)

# Check the result
if result.returncode == 0:
    print(f"Successfully pulled {repository_name}")
else:
    print("Error pulling the image:")
    print(result.stderr)
