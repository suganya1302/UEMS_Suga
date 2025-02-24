import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



stream_file_path = "Stream data.xlsx"
stream_data = pd.read_excel(stream_file_path, engine='openpyxl')
print(stream_data.iloc[:10, 5])  # First 10 rows, first 10 columns


#castle_file_path = "192 Castle street.xlsx"
#castle_data = pd.read_excel(castle_file_path, engine='openpyxl')
#print(castle_data .iloc[:10, 5])  # First 10 rows, first 10 columns


#janitza_file_path = "Janitza Reading.xlsx"
#janitza_data = pd.read_excel(janitza_file_path, engine='openpyxl')
#print(janitza_data .iloc[:10, 5])  # First 10 rows, first 10 columns


#gas_file_path = "Gas Data.xlsx"
#gas_data = pd.read_excel(gas_file_path, engine='openpyxl')
#print(gas_data.iloc[:10, 0])  # 9 to 19 (Python uses zero-based indexing)

#cfi_file_path = "CFI.xlsx"
#cfi_data = pd.read_excel(cfi_file_path , engine='openpyxl')
#print(cfi_data.iloc[:10, 9:20])  # 9 to 19 (Python uses zero-based indexing)

# ------- 🔍 Remove All "PF" Columns (Power Factor) ---------
pf_columns = [col for col in stream_data.columns if "PF" in col]
stream_data_filtered = stream_data.drop(columns=pf_columns)

print("\n✅ Removed Power Factor (PF) Columns. Remaining Columns:")
print(stream_data_filtered.columns)

# ------- 📊 Basic Dataset Information ---------
print("\n📝 Basic Information:")
print(stream_data_filtered.info())

print("\n📌 First Few Rows:")
print(stream_data_filtered.head())

# Check for missing values
print("\n🚨 Missing Values in Each Column:")
print(stream_data_filtered.isnull().sum())

# Summary statistics after PF removal
print("\n📊 Summary Statistics:")
print(stream_data_filtered.describe())

# Define column groups based on the screenshot
groups = {
    "Libraries": [
        "E902 Hocken Library - kWh", "F813 UOCOE Robertson Library - kWh",
        "D203 Sayers (at Adams) - kWh", "F813 Bill Robertson Library - kWh",
        "F419 ISB West Excludir - kWh", "F505 Richardson Library - kWh"
    ],
    "Colleges": [
        "C405 192 Castle College - kWh", "D402 Hayward College - kWh",
        "D40X Cumberland College - kWh", "F812 UOCOE Owheo Building - kWh",
        "G608 St Margarets College - kWh", "H41X Selwyn College - kWh E2",
        "H633 Arana College main - kWh", "H71X Studholm College - kWh E2",
        "J126 Carrington College (Kitchen/Dining) - kWh",
        "J14X Aquinas College - kWh", "J303 Caroline Freeman College - kWh",
        "K427 Abbey College - kWh"
    ],
    "Science": [
        "D403 Survey & Marine - kWh", "E212 Zoology Buildings - kWh",
        "F315 Botany Tin Hut - kWh", "F325 Physical Education - kWh",
        "F812 UOCOE Owheo Building - kWh", "G401 Mellor Laboratories - kWh",
        "G404 Microbiology - kWh", "G413 Science 2 - kWh",
        "J960 Portobello Marine Lab - kWh", "G505 Geology north:",
        "G505 Geology south:"
    ],
    "Health Science": [
        "A161 Taieri Farm - kWh", "D20X Med School Sub Main - kWh",
        "E214 Otago Dental School - kWh", "E301 Hunter Centre - kWh",
        "E305 Physiotherapy - kWh", "E325 Research Support Facility - kWh"
    ],
    "Humanities": [
        "F9XX College of Education main (Boiler room) - kWh",
        "F518 Arts 1 Submains MSB - kWh", "F516 97 Albany & F517 99 Albany - kWh",
        "F505 1 Richardson Mains - kWh", "G506/07 Archway buildings (incl. Allen & Marama Hall) - kWh"
    ],
    "Commerce": [
        "F614 1 School of Business Incomer 1 (Lower floors) - kWh",
        "F614 2 School of Business Incomer 2 (Upper floors) - kWh",
        "F618 1 Psychology substation - Goddard - kWh"
    ],
    "Total Electricity": [
        "Total Stream DN Electricity - kWh"
    ],
    "ITS Servers": [
        "F204 444 Great King Street - kWh", "325 Gt King Server (325-PHYS) - kWh"
    ]
}

# Perform correlation analysis for each group and plot heatmaps
for group_name, columns in groups.items():
    available_columns = [col for col in columns if col in stream_data_filtered.columns]
    
    if len(available_columns) > 1:  # Only process groups with more than one valid column
        plt.figure(figsize=(8,6))
        corr_matrix = stream_data_filtered[available_columns].corr(numeric_only=True)
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"Correlation Matrix: {group_name}")
        plt.show()
    else:
        print(f"\nSkipping {group_name} - Not enough valid columns for correlation analysis.")

# Iterate over each group and perform analyses
for group_name, columns in groups.items():
    available_columns = [col for col in columns if col in stream_data_filtered.columns]

    if len(available_columns) > 1:  # Only process groups with more than one valid column
        print(f"\n🔹 Analyzing {group_name} Group")

        # -------  Time Series Trend Analysis ---------
        plt.figure(figsize=(12,5))
        for col in available_columns:
            plt.plot(stream_data_filtered.index, stream_data_filtered[col], label=col, alpha=0.7)
        plt.xlabel("Time")
        plt.ylabel("Energy Consumption (kWh)")
        plt.title(f"Energy Consumption Over Time ({group_name})")
        plt.legend()
        plt.show()

        # ------- 🚨 Boxplot for Outlier Detection ---------
        plt.figure(figsize=(10,5))
        sns.boxplot(data=stream_data_filtered[available_columns])
        plt.xticks(rotation=90)
        plt.title(f"Boxplot of {group_name} Group (Outlier Detection)")
        plt.show()

        # ------- 📉 Histogram for Distribution ---------
        plt.figure(figsize=(8,5))
        for col in available_columns:
            sns.histplot(stream_data_filtered[col], bins=30, kde=True, label=col, alpha=0.5)
        plt.xlabel("Energy Consumption (kWh)")
        plt.ylabel("Frequency")
        plt.title(f"Distribution of Energy Consumption ({group_name})")
        plt.legend()
        plt.show()

        # ------- 🔍 Anomaly Detection using Z-score ---------
        z_scores = stream_data_filtered[available_columns].apply(lambda x: (x - x.mean()) / x.std())
        anomalies = z_scores[(z_scores.abs() > 3).any(axis=1)]

        # Plot anomalies
        plt.figure(figsize=(12,5))
        for col in available_columns:
            plt.scatter(stream_data_filtered.index, stream_data_filtered[col], label="Normal", color='blue', alpha=0.5)
            plt.scatter(anomalies.index, anomalies[col], color='red', label="Anomalies", marker='x')
        plt.xlabel("Time")
        plt.ylabel("Energy Consumption")
        plt.title(f"Anomaly Detection in {group_name} Group")
        plt.legend()
        plt.show()

    else:
        print(f"\nSkipping {group_name} - Not enough valid columns for analysis.")
