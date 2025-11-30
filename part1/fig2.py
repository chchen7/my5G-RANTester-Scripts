import csv
import matplotlib.pyplot as plt
import numpy as np


def sliding_window_mean(arr, window=5):
    arr = np.array(arr, dtype=float)
    if len(arr) < window:
        return arr  # not enough data, return as-is

    # Create sliding windows (NumPy 1.20+)
    windows = np.lib.stride_tricks.sliding_window_view(arr, window)
    smooth = np.nanmean(windows, axis=1)

    return smooth

base_filename = '../history/my5grantester-logs-1-{}-{}-{}.csv'
cores = [2, 3]
cores_name = ['free5GC', 'Open5GS']
execs = [500, 400, 300, 200, 100]     # delays in ms
experiments = [1, 3, 5, 7, 9, 11]           # gNB counts

MAX_AXIS_X = 5
# MAX_AXIS_Y = 3

plt.rcParams["figure.figsize"] = (6, 10)
# compress x axis length
plt.rcParams['figure.subplot.hspace'] = 0.5
for core_idx, core in enumerate(cores):

    axis_x = 0
    axis_y = 0
    figure, axis = plt.subplots(MAX_AXIS_X,1)
    figure.canvas.manager.set_window_title(cores_name[core_idx])

    for exe in execs:
        for exp in experiments:

            time_base = 0
            timestamp = np.array([])
            dataplaneready = np.array([])

            with open(base_filename.format(core, exe, exp), newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if time_base == 0:
                        time_base = int(row['timestamp'])

                    try:
                        dataplaneready = np.append(dataplaneready,
                                                   float(row['DataPlaneReady']))
                        timestamp = np.append(timestamp,
                                    (int(row['timestamp']) - time_base) / 1_000_000_000)
                    except:
                        continue

            smooth_dp = sliding_window_mean(dataplaneready)
            smooth_ts = timestamp[len(timestamp) - len(smooth_dp):]
            
            KEEP_RATIO = 0.2   # keep 10%
            mask = np.random.rand(len(smooth_ts)) < KEEP_RATIO

            smooth_ts = smooth_ts[mask]
            smooth_dp = smooth_dp[mask]

            axis[axis_x].scatter(
                smooth_ts,
                smooth_dp,
                # label="#gNB {}".format(exp),
                s=3
            )

        axis[axis_x].set_title("{} (Delay {})".format(cores_name[core_idx], exe))

        axis_x += 1

    figure.legend()
    plt.savefig('experiment_1_{}.png'.format(cores_name[core_idx]))

