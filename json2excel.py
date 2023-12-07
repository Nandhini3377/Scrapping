import pandas as pd
import json

def convert_json_to_xlsx(json_file, xlsx_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Assuming data is a list of dictionaries, each representing a row
    df = pd.DataFrame(data)

    # Write DataFrame to Excel file
    df.to_excel(xlsx_file, index=False)

# Example usage
# json_filename = 'dump4.json'  # Replace with your JSON file
# xlsx_filename = 'output.xlsx'  # Replace with your desired output XLSX file

# convert_json_to_xlsx(json_filename, xlsx_filename)
