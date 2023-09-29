import json
import os
from ena_objects.ena_submission import EnaSubmission

# Read json file
isa_json_file = open("tests/test_data/isa_json_test_investigation.json")
isa_json = json.load(isa_json_file)

# Change this to 'True' if you want to export the resulting DataFrames to an xlsx.
export_to_excel = False
outputfolder = "./output_folder/"

submission = EnaSubmission.from_isa_json(isa_json)
submission_dfs = submission.generate_dataframes()

if (not os.path.exists(outputfolder)) and export_to_excel:
    os.makedirs(outputfolder)

for k, df in submission_dfs.items():
    print(f"Dataframe {k}:")
    print(df)
    if export_to_excel:
        df.to_excel(f"{outputfolder}{k}.xlsx")

print("Done!")
