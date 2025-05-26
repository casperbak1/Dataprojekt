import pandas as pd
import numpy as np
import os
import re


# === Input/Output paths ===
input_csv = os.path.join("Pipeline_data", "Output_after_pixel_matrix", "Predicted_keypoints_pixel_matrix.csv")
output_csv = os.path.join("Pipeline_data", "patient_level_summary4.csv")

# === Load data ===
print("Loading data...")
df = pd.read_csv(input_csv)
df["Filename"] = df["Filename"].str.replace(".png", "", regex=False)

# === Extract metadata ===
print("Extracting metadata from filenames...")
df["Jaw"] = df["Filename"].str.extract(r"(Upper|Lower)", flags=re.IGNORECASE)[0].str.lower()
df["Suffix"] = df["Filename"].str.extract(r"_([a-zA-Z0-9]+)$")[0].str.lower()
df["Base_ID"] = df["Filename"].str.extract(r"^([A-Za-z0-9]+)")[0]

# === Separate upper and lower entries
print("Separating upper and lower jaw entries...")
df_upper = df[df["Jaw"] == "upper"][["Base_ID", "Suffix", "Y_Refined"]].rename(columns={"Y_Refined": "Y_upper"})
df_lower = df[df["Jaw"] == "lower"][["Base_ID", "Suffix", "Y_Refined"]].rename(columns={"Y_Refined": "Y_lower"})

# === Merge to align upper/lower by suffix
print("Merging upper and lower jaw data by Base_ID and Suffix...")
df_merge = pd.merge(df_upper, df_lower, on=["Base_ID", "Suffix"])
print(f"Found {len(df_merge)} matched upper-lower pairs.")

# === Compute overbite
print("Calculating overbite for each pair...")
df_merge["overbite_mm"] = (df_merge["Y_lower"] - df_merge["Y_upper"]) * 0.08
df_merge["overbite_pixel"] = df_merge["Y_lower"] - df_merge["Y_upper"]
print(df_merge[["Base_ID", "Suffix", "Y_upper", "Y_lower", "overbite_pixel", "overbite_mm"]])

# === Compute average overbite per patient
print("Averaging overbite per patient...")
df_avg = df_merge.groupby("Base_ID", as_index=False).agg({
    "overbite_mm": "mean",
    "overbite_pixel": "mean"
})

# === Classify based on overbite
def classify_overbite(mm):
    if pd.isna(mm):
        return ""
    if mm < 1:
        return "A"
    elif mm < 2:
        return "B"
    elif mm < 3:
        return "C"
    elif mm < 4:
        return "D"
    else:
        return "E"

df_avg["Predicted_Class"] = df_avg["overbite_mm"].apply(classify_overbite)

# === Prepare final output
df_patient_summary = df_avg.rename(columns={
    "Base_ID": "Filename",
    "overbite_pixel": "Overbite_pixel_AVG",
    "overbite_mm": "Overbite_mm_AVG"
})[["Filename", "Overbite_pixel_AVG", "Overbite_mm_AVG", "Predicted_Class"]]

print("\nFinal summary:")
print(df_patient_summary)

# === Save result
df_patient_summary.to_csv(output_csv, index=False)
print(f"\n✅ Patient-level summary saved to: {output_csv}")