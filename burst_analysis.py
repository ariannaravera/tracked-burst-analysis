import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import os


def count_consec(lst):
    """
    Counts the number of consecutive repetitions in lst.
    Input:
        lst - list of numbers
    Output:
        consec - number of consecutive repetitions
        initials - initial value for each repetition found
    """
    lst.sort()
    consec = [1]
    for x, y in zip(lst, lst[1:]):
        if x == y - 1:
            consec[-1] += 1
        else:
            consec.append(1)
    
    initials = []
    pos = 0
    for i, v in enumerate(consec):
        if i == 0:
            initials.append(lst[0])     
        else:
            initials.append(lst[pos])
        pos += v
    return consec, initials


def filter_dataframe(original_df, output_path):
    """
    Filters the dataframe keeping only bursts/spots in cell areas
    sorts the dataframe based on the TRACK_ID column and casts some of its columns
    Input:
        original_df - original dataframe
        output_path - path to output
    Output:
        filtered_df - filtered dataframe
    Save:
        filtered_tracking_output.csv - filtered dataframe
    """
    # Remove first 3 "empty" rows
    filtered_df = original_df.iloc[3:,:].copy()
    # Convert MAX_INTENSITY_CH3 column to integer
    filtered_df['MAX_INTENSITY_CH3'] = pd.to_numeric(filtered_df['MAX_INTENSITY_CH3']).astype('Int64')
    # Filter MAX_INTENSITY_CH3 column equal to 1 (and so in the cell -> 1=cell, 2=nucleo, 3=background - from ilastik output)
    filtered_df = filtered_df.loc[filtered_df['MAX_INTENSITY_CH3']==1]
    # Convert MAX_INTENSITY_CH2 column to integer
    filtered_df['MAX_INTENSITY_CH2'] = pd.to_numeric(filtered_df['MAX_INTENSITY_CH2']).astype('Int64')
    # Set TRACK_ID equal to MAX_INTENSITY_CH2
    filtered_df['TRACK_ID']  = filtered_df['MAX_INTENSITY_CH2']
    # Sort based on TRACK_ID values
    filtered_df = filtered_df.sort_values("TRACK_ID")
    # Convert POSITION_T column to integer for further analysis
    filtered_df['POSITION_T'] = pd.to_numeric(filtered_df['POSITION_T']).astype('Int64')
    # Save the filtered dataframe to csv file named "filtered_tracking_output.csv"
    filtered_df.to_csv(os.path.join(output_path, 'filtered_tracking_output.csv'), index=True)

    return filtered_df


def main(input_data_path, output_path):
    # Reading csv file 
    original_df = pd.read_csv(input_data_path)

    # Filter the dataframe with only bursts in cells areas
    filtered_df = filter_dataframe(original_df, output_path)

    # Create the "bursts_info.csv" in which to save results
    with open(os.path.join(output_path, 'bursts_info.csv'), "w") as file:
        writer = csv.writer(file)
        writer.writerow(['Burst id', 'ON[min]', 'OFF[min]', 'frames ON', 'frames OFF'])

    max_duration = 0

    fig, ax = plt.subplots(figsize=(16, 3))
    
    # Count positive and negative periods per burst
    for id in np.unique(filtered_df['TRACK_ID']):
        # Read time frames in which we had this burst
        tps_ON = list(filtered_df.loc[filtered_df['TRACK_ID'] == id, 'POSITION_T'])
        # Calculate the consecutive ON time frames minutes (each timeframe corresponds to 2min)
        tps_ON_duration, initials = [x*2 for x in count_consec(tps_ON)]
        
        # Calculate time frames in which we did had this burst
        tps_OFF = [x for x in np.arange(min(tps_ON), max(tps_ON)) if x not in tps_ON]
        # If there are OFF time frames
        if len(tps_OFF) > 0:
            # Calculate the consecutive OFF time frames minutes (each timeframe corresponds to 2min)
            tps_OFF_duration, _ = [x*2 for x in count_consec(tps_OFF)]
        # Otherwise set OFF time frames duration to empty
        else:
            tps_OFF_duration = []

        # Save results in bursts_info.csv file
        with open(os.path.join(output_path, 'bursts_info.csv'), "a") as file:
            writer = csv.writer(file)
            writer.writerow([id, tps_ON_duration, tps_OFF_duration, tps_ON, tps_OFF])
        
        if tps_ON[-1] + tps_ON_duration[-1] > max_duration:
            max_duration = tps_ON[-1] + tps_ON_duration[-1]
            
        # Set values for the plot: list of tuples with the initial burst tp and its duration
        plot_values = []
        for i in range(len(tps_ON)):
            plot_values.append((initials[i], tps_ON_duration[i]))
        
        # Plot burst duration
        ax.broken_barh(plot_values, (id-0.1, 0.2))
    
    # Set plot info
    ax.set_yticks(np.unique(filtered_df['TRACK_ID']))
    ax.set_ylabel("Burst ID")
    ax.set_xlabel("Time points[min]")
    ax.set_xticks(range(1, max_duration+1))
    ax.set_xlim([1, max_duration+1])
    ax.set_ylim([0, max(np.unique(filtered_df['TRACK_ID']))+1])
    plt.grid(alpha=0.6)
    plt.tight_layout()       
    plt.savefig(os.path.join(output_path, 'burst_spots_duration.png'))


if __name__=='__main__':
    ### PARAMS TO CHANGE ###

    # Path of the initial csv file (from TrackMate)
    input_data_path = './data/complete_tracking_result.csv'
    # Path of the folder in which to save the outputs
    output_path = './results'

    ### RUN ###
    main(input_data_path, output_path)
    