# Analysis of TrackMate results

## Overview

This script processes the results obtained from TrackMate, a popular tracking software used for particle tracking in biological imaging. The script filters the data and generates visualizations to help understand the dynamics of burst spots within cells over time.

## Features

- Reads the TrackMate result dataframe.
- Filters the data to identify relevant burst spots.
- Produces CSV files summarizing the presence and duration of burst spots in cells.
- Generates graphs to visualize:
  - The number of time frames burst spots are present.
  - The duration of burst spots within the cells.

## Requirements

- Python 3.11
- Pandas
- Matplotlib
- Numpy
- Csv

## Installation

To install the required packages, you can use pip:

```bash
pip install pandas matplotlib numpy csv
```

## Usage

1. Modify line 133 and 135 with the input path of TrackMate result dataframe file (e.g., ./data/trackmate_results.csv) and the output path where you want to save results.
2. Run 
```bash
python burst_analysis.py
```

## Output

- **CSV Files**: The script will generate CSV files summarizing the presence and duration of burst spots.
- **Graphs**: The script will produce graphs showing:
  - The number of time frames burst spots are present in cells.
  - The duration of burst spots.

## Example

Running the script will produce:
- `filtered_tracking_output.csv`: Filtered dataframe with relevant burst spots.
- `bursts_info.csv`: Duration and timeframes in which the burst spot is active and is not.
- `burst_spots_duration.png`: Graph showing the duration of burst spots in cells.
![burst_spots_duration](https://github.com/ariannaravera/tracked-burst-analysis/assets/48065927/780c6e8d-3048-4c0e-9228-c373f323f9ce)

## Script Details

The script performs the following steps:

1. **Read the TrackMate Results**: Loads the TrackMate results into a pandas dataframe.
2. **Filter the Data**: Applies filtering criteria to isolate burst spots of interest.
3. **Analyze and Summarize**: Computes the presence and duration of burst spots.
4. **Generate Outputs**: Produces CSV files and visualizations to summarize the analysis.

## Contact

For any questions or issues, please contact Arianna Ravera at ariannaravera22@gmail.com.

---

This README provides a comprehensive guide to using the TrackMate Analysis Script for filtering and visualizing burst spot data.
