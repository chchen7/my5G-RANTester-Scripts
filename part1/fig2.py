import csv
import matplotlib.pyplot as plt
import numpy as np


def sliding_window_mean(arr, window=5):
    arr = np.array(arr, dtype=float)
    if len(arr) < window:
        return arr
    
    windows = np.lib.stride_tricks.sliding_window_view(arr, window)
    smooth = np.nanmean(windows, axis=1)

    return smooth

base_filename = '../history/my5grantester-logs-{}-{}-{}-{}.csv'
cores = [2, 3]
cores_name = ['free5GC', 'Open5GS']
execs = list(range(1, 11)) 
delays = [ 500, 400, 300, 200, 100 ]     # delays in ms
experiments = [1, 3, 5, 7, 9, 11]           # gNB counts

data_free5gc = {}
data_open5gs = {}

MAX_AXIS_X = 5
MAX_AXIS_Y = 2

plt.rcParams["figure.figsize"] = (12, 10)
plt.rcParams['figure.subplot.hspace'] = 0.5
plt.rcParams['figure.subplot.wspace'] = 0.3

figure, axis = plt.subplots(MAX_AXIS_X, MAX_AXIS_Y)

for core_idx, core in enumerate(cores):

    axis_x = 0
    axis_y = core_idx  # Offset columns for second core

    for delay in delays:
        for exp in experiments:
            all_dataplaneready = []
            # print("Processing core {}, delay {}, exp {}".format(cores_name[core_idx], delay, exp))
            for exe in execs:
                try:
                    dataplaneready = np.array([])
                    timestamp = np.array([])
                    time_base = 0
                    with open(base_filename.format(exe, core, delay, exp), newline='') as csvfile:
                        reader = csv.DictReader(csvfile)

                        for row in reader:
                            if time_base == 0:
                                time_base = int(row['timestamp'])

                            try:
                                dataplaneready = np.append(dataplaneready, float(row['DataPlaneReady']))
                                timestamp = np.append(timestamp, (int(row['timestamp']) - time_base) / 1_000_000_000)
                            except:
                                continue
                    # print(len(dataplaneready), end=",")
                    all_dataplaneready.append((dataplaneready, timestamp))
                except FileNotFoundError:
                    continue
            # print()
            if not all_dataplaneready:
                continue
            
            # Find the longest execution
            longest_idx = max(range(len(all_dataplaneready)), key=lambda i: len(all_dataplaneready[i][0]))
            max_len = len(all_dataplaneready[longest_idx][0])
            timestamp = all_dataplaneready[longest_idx][1]  # Use timestamp from longest execution
            
            # Pad all dataplaneready arrays to same length with NaN
            padded_data = []
            for dp, ts in all_dataplaneready:
                if len(dp) < max_len:
                    padded = np.pad(dp, (0, max_len - len(dp)), constant_values=np.nan)
                else:
                    padded = dp
                padded_data.append(padded)
            
            # Average across executions (ignoring NaN)
            avg_dp = np.nanmean(padded_data, axis=0)
            
            smooth_dp = sliding_window_mean(avg_dp)
            smooth_ts = timestamp[len(timestamp) - len(smooth_dp):]
            
            KEEP_RATIO = 1   # keep 100%
            mask = np.random.rand(len(smooth_ts)) < KEEP_RATIO

            smooth_ts = smooth_ts[mask]
            smooth_dp = smooth_dp[mask]

            # Use the correct column offset for each core
            current_axis_y = axis_y + (axis_x // MAX_AXIS_X)
            current_axis_x = axis_x % MAX_AXIS_X
            
            axis[current_axis_x, current_axis_y].scatter(
                smooth_ts,
                smooth_dp,
                label= "#gNB {}".format(exp),
                s=3
            )
            if(axis_x == 1 and axis_y == 1):
                axis[axis_x, axis_y].legend(fontsize=10, markerscale=2, bbox_to_anchor=(1.05, 1), loc='upper left')

        axis[axis_x, axis_y].set_title("{} (Delay {})".format(cores_name[core_idx], delay))

        axis_x += 1
        if (axis_x >= MAX_AXIS_X):
            axis_x = 0
            axis_y += 1

plt.tight_layout()  # Adjust spacing to prevent overlap
plt.savefig('fig2.png')
plt.close(figure)