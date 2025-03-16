import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub

# Set style for plots
plt.style.use('fivethirtyeight')
sns.set(font_scale=1.2)

# Create a directory for saving figures
os.makedirs('serial_killer_figures', exist_ok=True)

# Download dataset
print("Downloading serial killers dataset...")
path = kagglehub.dataset_download("vesuvius13/serial-killers-dataset")
print(f"Dataset downloaded to: {path}")

# Load the dataset
# Assuming the CSV file is in the downloaded directory
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
if not csv_files:
    raise FileNotFoundError("No CSV files found in the downloaded dataset")

# Print available files to identify the correct one
print(f"Available files: {os.listdir(path)}")

# Let's try to load the first CSV file
killers_data = pd.read_csv(os.path.join(path, csv_files[0]))

# Display basic info about the dataset
print("\nDataset Overview:")
print(f"Shape: {killers_data.shape}")
print("\nColumns:")
print(killers_data.columns.tolist())
print("\nSample data:")
print(killers_data.head())

# Check for missing values
print("\nMissing values:")
print(killers_data.isnull().sum())

# Function to save figures
def save_figure(fig, filename):
    fig.savefig(os.path.join('serial_killer_figures', filename), bbox_inches='tight', dpi=300)
    plt.close(fig)

# Clean and prepare data
# Assuming column names for victims and country - these will be adjusted based on actual data
# Try to find victim count column
victim_columns = [col for col in killers_data.columns if any(word in col.lower() for word in ['victim', 'kill', 'death', 'body'])]
if victim_columns:
    victim_column = victim_columns[0]
    print(f"\nFound victim count column: {victim_column}")
else:
    # Try to infer it from numerical columns
    numerical_cols = killers_data.select_dtypes(include=[np.number]).columns.tolist()
    if numerical_cols:
        print(f"No obvious victim column found. Using numerical column: {numerical_cols[0]}")
        victim_column = numerical_cols[0]
    else:
        raise ValueError("Could not identify a column for victim counts")

# Try to find country column
country_columns = [col for col in killers_data.columns if any(word in col.lower() for word in ['country', 'nation', 'location'])]
if country_columns:
    country_column = country_columns[0]
    print(f"Found country column: {country_column}")
else:
    print("No country column identified. Looking for country names in other text columns...")
    # Implement more sophisticated country detection here if needed
    country_column = None

# Analysis 1: Top 10 most deadly serial killers by proven victims
try:
    # Convert victim count to numeric if it's not already
    if not pd.api.types.is_numeric_dtype(killers_data[victim_column]):
        killers_data[victim_column] = pd.to_numeric(killers_data[victim_column], errors='coerce')
    
    # Sort by victim count and get top 10
    top_killers = killers_data.sort_values(by=victim_column, ascending=False).head(10)
    
    # Get name column (assuming it has 'name' in it or is the first string column)
    name_columns = [col for col in killers_data.columns if 'name' in col.lower()]
    if name_columns:
        name_column = name_columns[0]
    else:
        # Use first string column as name
        string_cols = killers_data.select_dtypes(include=['object']).columns
        name_column = string_cols[0] if len(string_cols) > 0 else killers_data.columns[0]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=victim_column, y=name_column, data=top_killers, ax=ax)
    ax.set_title('Top 10 Most Deadly Serial Killers by Proven Victims')
    ax.set_xlabel('Number of Victims')
    ax.set_ylabel('Killer Name')
    
    # Save figure
    save_figure(fig, 'top10_deadliest_killers.png')
    print("Top 10 most deadly serial killers plot saved")
except Exception as e:
    print(f"Error in analysis 1: {e}")

# Analysis 2: Top 5 serial killers just in the US
if country_column:
    try:
        # Filter for US killers
        us_killers = killers_data[killers_data[country_column].str.contains('US|United States|USA', case=False, na=False)]
        
        # Sort by victim count and get top 5
        top_us_killers = us_killers.sort_values(by=victim_column, ascending=False).head(5)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=victim_column, y=name_column, data=top_us_killers, ax=ax)
        ax.set_title('Top 5 Most Deadly Serial Killers in the US')
        ax.set_xlabel('Number of Victims')
        ax.set_ylabel('Killer Name')
        
        # Save figure
        save_figure(fig, 'top5_us_killers.png')
        print("Top 5 US serial killers plot saved")
    except Exception as e:
        print(f"Error in analysis 2: {e}")
else:
    print("Cannot perform US-specific analysis without country information")

# Analysis 3: Top 5 countries with serial killers
if country_column:
    try:
        # Count killers by country
        country_counts = killers_data[country_column].value_counts().head(5)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 8))
        country_counts.plot(kind='bar', ax=ax)
        ax.set_title('Top 5 Countries with Most Serial Killers')
        ax.set_xlabel('Country')
        ax.set_ylabel('Number of Serial Killers')
        
        # Save figure
        save_figure(fig, 'top5_countries.png')
        print("Top 5 countries with serial killers plot saved")
    except Exception as e:
        print(f"Error in analysis 3: {e}")
else:
    print("Cannot perform country analysis without country information")

print("\nSerial killers analysis completed!") 