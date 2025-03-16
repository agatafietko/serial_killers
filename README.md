# Serial Killers Analysis

This project analyzes the "Serial Killers Dataset" from Kaggle to visualize and understand patterns related to serial killers across different regions.

## Analyses Performed

1. **Top 10 Most Deadly Serial Killers**: Visualization of serial killers with the highest number of proven victims.
2. **Top 5 Serial Killers in the US**: Visualization focusing on the deadliest serial killers in the United States.
3. **Top 5 Countries with Serial Killers**: Visualization showing which countries have the highest counts of serial killers.

## Requirements

- Python 3.6+
- Required packages:
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - kagglehub

You can install all requirements using:
```
pip install -r requirements.txt
```

## Dataset

The dataset is downloaded automatically from Kaggle using the kagglehub library:
```python
kagglehub.dataset_download("vesuvius13/serial-killers-dataset")
```

## Usage

Simply run the Python script:
```
python serial_killers_analysis.py
```

The script will:
1. Download the dataset from Kaggle
2. Process the data
3. Generate visualizations in the `serial_killer_figures` directory

## Outputs

All visualizations are saved in the `serial_killer_figures` directory:
- `top10_deadliest_killers.png`: Bar chart of serial killers with the most victims
- `top5_us_killers.png`: Bar chart of the deadliest serial killers in the US
- `top5_countries.png`: Bar chart of countries with the most serial killers

If a specific column isn't found in the dataset, the script will try to use alternatives or proxies based on the available data.

## Note

The script is designed to be adaptive, as the column names in the dataset may vary. It will try to identify the most appropriate columns for the analyses based on keywords in the column names.

## Disclaimer

This analysis is purely for academic and educational purposes. The subject matter is sensitive, and the data is presented objectively without any intent to glorify or sensationalize crime. 