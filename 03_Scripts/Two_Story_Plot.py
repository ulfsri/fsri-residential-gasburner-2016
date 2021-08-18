# Experiment Plotter 2015 NIJ Two Story

# --------------- #
# Import Packages #
# --------------- #
import os
import socket
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Set seaborn as default plot config
sns.set()
sns.set_style("whitegrid")
from cycler import cycler
from itertools import cycle
from pathlib import Path

# ---------------------------------- #
# Define Subdirectories & Info Files #
# ---------------------------------- #

data_dir = '../01_Data/Two_Story/'
info_dir = '../02_Info/'
plot_dir = '../04_Charts/Two_Story/'

# Create plot dir if necessary
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Read in exp info file
exp_info = pd.read_csv(f'{info_dir}Info_Two_Story.csv', index_col='Test_Name')

# ------------------- #
# Set Plot Parameters #
# ------------------- #

label_size = 16
tick_size = 16
line_width = 1.5
event_font = 12
font_rotation = 60
legend_font = 13
fig_width = 10
fig_height = 8

# ---------------------- #
# User-Defined Functions #
# ---------------------- #
def timestamp_to_seconds(timestamp):
    timestamp = timestamp[11:]
    hh, mm, ss = timestamp.split(':')
    return(3600 * int(hh) + 60 * int(mm) + int(ss))

def convert_timestamps(timestamps, start_time):
    raw_seconds = map(timestamp_to_seconds, timestamps)
    return([s - start_time for s in list(raw_seconds)])

def create_1plot_fig():
    # Define figure for the plot
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    # Set line colors & markers; reset axis lims
    current_palette_8 = sns.color_palette('deep', 8)
    sns.set_palette(current_palette_8)

    plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v', '8', 'D', '*', '<', '>', 'H'])
    x_max, y_min, y_max = 0, 0, 0

    return(fig, ax1, plot_markers, x_max, y_min, y_max)

def format_and_save_plot(y_lims, x_lims, secondary_axis_label, file_loc):
    # Set tick parameters
    ax1.tick_params(labelsize=tick_size, length=0, width=0)

    # Scale axes limits & labels
    ax1.grid(True)
    ax1.set_ylim(bottom=y_lims[0], top=y_lims[1])
    ax1.set_xlim(x_lims[0] - x_lims[1] / 400, x_lims[1])
    ax1.set_xlabel('Time (s)', fontsize=label_size)

    # Secondary y-axis parameters
    if secondary_axis_label != 'None':
        ax2 = ax1.twinx()
        ax2.tick_params(labelsize=tick_size, length=0, width=0)
        ax2.set_ylabel(secondary_axis_label, fontsize=label_size)
        if secondary_axis_label == 'Temperature ($^\circ$F)':
            ax2.set_ylim([y_lims[0] * 1.8 + 32., y_lims[1] * 1.8 + 32.])
        else:
            ax2.set_ylim([secondary_axis_scale * y_lims[0],
                            secondary_axis_scale * y_lims[1]])
        ax2.yaxis.grid(b=None)

    # Add vertical lines and labels for timing information (if available)
    ax3 = ax1.twiny()
    ax3.set_xlim(x_lims[0] - x_lims[1] / 400, x_lims[1])
    ax3.set_xticks([_x for _x in Events.index.values if _x >= x_lims[0] and _x <= x_lims[1]])
    ax3.tick_params(axis='x', width=1, labelrotation=font_rotation, labelsize=event_font)
    ax3.set_xticklabels([Events['Event'][_x] for _x in Events.index.values if _x >= x_lims[0] and _x <= x_lims[1]], fontsize=event_font, ha='left')
    ax3.xaxis.grid(b=None)

    # Add legend, clean up whitespace padding, save chart as pdf, & close fig
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(handles1, labels1, loc='best', fontsize=legend_font, handlelength=3, frameon=True, framealpha=0.75)

    fig.tight_layout()
    plt.savefig(file_loc)
    plt.close()

# -------------------------------------- #
# Start Code Used to Generate Data Plots #
# -------------------------------------- #
data_file_ls = [f'{exp}.csv' for exp in exp_info.index.values.tolist()]

# Loop through test data files & create plots
for f in data_file_ls:

    # Read in data for experiment, rename time column to timestamp
    data_df = pd.read_csv(f'{data_dir}{f}')
    data_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    data_df = data_df.set_index('Time')

    if Path(f'{data_dir}{f[:-4]}_Event.csv').is_file():
        Events = pd.read_csv(f'{data_dir}{f[:-4]}_Event.csv')

    # Get test name from file
    test_name = f[:-4]
    print (f'--- Loaded data file for {test_name} ---')

    # Read in channel list file & create list of sensor groups
    channel_list = pd.read_csv(info_dir+'Channel_list_Two_Story.csv', index_col='Channel_Name')
    channel_groups = channel_list.groupby('Group')

    # Create index column of time relative to ignition in exp_data
    Events = pd.read_csv(f'{data_dir}{f[:-4]}_Events.csv')
    Events.rename(columns={'Time':'Timestamp'}, inplace=True)
    event_idx_ls = Events[pd.notna(Events['Event'])].index.values
    ignition_idx = int(exp_info.at[test_name, 'Ignition_Event'])
    start_timestamp = Events.loc[event_idx_ls[ignition_idx], 'Timestamp'].split(' ')[-1]
    start_timestamp = start_timestamp[11:]
    hh,mm,ss = start_timestamp.split(':')
    start_time = 3600 * int(hh) + 60 * int(mm) + int(ss)
    Events['Time'] = convert_timestamps(Events['Timestamp'], start_time)
    Events = Events.set_index('Time')
    # Loop through channel groups & generate plot of channel data
    for group in channel_groups.groups:

        print (f"  Plotting {group.replace('_',' ')}")

        # Create figure for plot(s)
        fig, ax1, plot_markers, x_max, y_min, y_max = create_1plot_fig()

        # Plot each channel within group
        for channel in channel_groups.get_group(group).index.values:

            # Set secondary axis default to None, get data type from channel list
            secondary_axis_label = 'None'
            data_type = channel_list.loc[channel, 'Type']

            # Set plot parameters based on data type
            if data_type == 'Temperature':

                # Set y-axis labels & limits
                ax1.set_ylabel('Temperature ($^\circ$C)', fontsize=label_size)
                secondary_axis_label = 'Temperature ($^\circ$F)'
                y_min = 0
                y_max= exp_info['Y Scale TC'][test_name]

            elif data_type == 'Velocity':

                # Set y-axis labels, secondary scale, & limits
                ax1.set_ylabel('Velocity (m/s)', fontsize=label_size)
                secondary_axis_label = 'Velocity (mph)'
                secondary_axis_scale = 2.23694
                y_max= exp_info['Y Scale BDP'][test_name]

            elif data_type == 'Pressure':

                # Set y-axis label, secondary scale, & limits
                ax1.set_ylabel('Pressure (Pa)', fontsize=label_size)
                secondary_axis_label = 'Pressure (psi)'
                secondary_axis_scale = 0.000145038
                y_max= exp_info['Y Scale PRESSURE'][test_name]

            # Determine x bounds for current data & update max of chart if necessary
            x_min = 0
            x_end = exp_info['End_Time'][test_name]
            if x_end > x_max:
                x_max = x_end

            # Plot channel data
            ax1.plot(data_df.index, data_df[channel], lw=line_width,
                marker=next(plot_markers), markevery=30, mew=3, mec='none', ms=7, 
                label=channel_list.loc[channel, 'Channel_Label'])

            if data_type== 'Velocity' or data_type== 'Pressure':
                y_min = -1*y_max
            else:
                y_min = 0

        # Add vertical lines for event labels; label to y axis
        [ax1.axvline(_x, color='0.25', lw=1) for _x in Events.index.values if _x >= 0 and _x <= x_max]

        # Set save directory and call plotting function
        save_dir = f'{plot_dir}{test_name}/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        format_and_save_plot([y_min, y_max], [x_min, x_max], secondary_axis_label, f'{save_dir}{group}.pdf')
