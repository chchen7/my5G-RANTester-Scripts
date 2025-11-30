import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import csv
import statistics
import os 
INITIAL_UE = 43
UE_PER_GNB = 100

vm_configs = [ "TG2-12C-8GB" ]
cores_name = [ 'free5GC', 'Open5GS' ]
cores = [ 2, 3 ]
execs = list(range(1, 11))              # Executions 1 to 10
# execs = [1]
delays = [ 500, 400, 300, 200, 100 ]    # Delays between connections in ms
experiments = [ 1, 3, 5, 7, 9, 11 ]     # Experiments 1 to 11, step 2

# rng = np.random.default_rng(0)
# data_free5gc = {
#     lat: [rng.uniform(0, 100, size=rng.integers(5, 10)) for _ in experiments]
#     for lat in delays
# }

# data_open5gs = {
#     lat: [rng.uniform(0, 100, size=rng.integers(5, 10)) for _ in experiments]
#     for lat in delays
# }
data_free5gc = {}
data_open5gs = {}

# print shape of data shape
# print("free5GC data shape:")
# for lat in delays:
#     for i, d in enumerate(data_free5gc[lat]):
#         print(f"Delay {lat} ms, Experiment {experiments[i]}: {d.shape}")
#         print("Data:", d)

for vm in vm_configs:
    base_filename = "my5grantester-logs-{}-{}-{}-{}.csv"

    for core_idx, core in enumerate(cores):
        for delay in delays:
            for exp in experiments:
                for exe in execs:
                    time_base = 0
                    fails_counter = 0
                    try:
                        input_filename = base_filename.format(exe, core, delay, exp)
                        with open(input_filename, newline='') as csvfile:
                            reader = csv.DictReader(csvfile)
                            # if DataPlaneReady NaN count as failed connection
                            for row in reader:
                                if time_base == 0:
                                    time_base = int(row['timestamp'])
                                
                                try:
                                    dataplaneready = float(row['DataPlaneReady'])
                                    if np.isnan(dataplaneready):
                                        fails_counter += 1
                                except:
                                    fails_counter += 1
                    except Exception as e:
                        print("Error reading file: " + e.__str__() + " " + input_filename)
                        continue
                    total_ue = exp * UE_PER_GNB
                    fail_rate = (fails_counter / total_ue) * 100
                    if core == 2:
                        if delay not in data_free5gc:
                            data_free5gc[delay] = [[] for _ in experiments]
                        data_free5gc[delay][experiments.index(exp)].append(fail_rate)
                    else:
                        if delay not in data_open5gs:
                            data_open5gs[delay] = [[] for _ in experiments]
                        data_open5gs[delay][experiments.index(exp)].append(fail_rate)

# print out all data collected
print("free5GC data collected:")
for lat in delays:
    for i, d in enumerate(data_free5gc[lat]):
        print(f"Delay {lat} ms, Experiment {experiments[i]}: {d}")
        print("Data:", d)
print("Open5GS data collected:")
for lat in delays:
    for i, d in enumerate(data_open5gs[lat]):
        print(f"Delay {lat} ms, Experiment {experiments[i]}: {d}")
        print("Data:", d)
# exit()

fig, axes = plt.subplots(
    nrows=len(delays),
    ncols=1,
    figsize=(9, 10),
    sharex=True
)

colors = {
    "free5GC": "#f5a623",
    "Open5GS": "#4a90e2"
}

for ax, lat in zip(axes, delays):
    ax.boxplot(
        data_free5gc[lat],
        positions=np.arange(len(experiments)) - 0.15,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='none', color=colors["free5GC"]),
        capprops=dict(color=colors["free5GC"]),
        whiskerprops=dict(color=colors["free5GC"]),
        flierprops=dict(marker='o', markerfacecolor='none',
                        markeredgecolor=colors["free5GC"]),
        medianprops=dict(color=colors["free5GC"])
    )
    for i, d in enumerate(data_free5gc[lat]):
        x = np.full(len(d), i - 0.15)
        ax.scatter(x, d, edgecolor=colors["free5GC"],
                   facecolor='none', s=40)


    ax.boxplot(
        data_open5gs[lat],
        positions=np.arange(len(experiments)) + 0.15,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='none', color=colors["Open5GS"]),
        capprops=dict(color=colors["Open5GS"]),
        whiskerprops=dict(color=colors["Open5GS"]),
        flierprops=dict(marker='o', markerfacecolor='none',
                        markeredgecolor=colors["Open5GS"]),
        medianprops=dict(color=colors["Open5GS"])
    )


    for i, d in enumerate(data_open5gs[lat]):
        x = np.full(len(d), i + 0.15)
        ax.scatter(x, d, edgecolor=colors["Open5GS"],
                   facecolor='none', s=40)

    ax.set_ylabel("Error rate (%)")
    ax.set_title(f"{lat} ms", fontsize=12)
    ax.set_ylim(0, 110)

# Shared x-axis
axes[-1].set_xticks(np.arange(len(experiments)))
axes[-1].set_xticklabels(experiments)
axes[-1].set_xlabel("Number of gNBs per core")

legend_patches = [
    Patch(facecolor='none', edgecolor=colors["free5GC"], label='free5GC'),
    Patch(facecolor='none', edgecolor=colors["Open5GS"], label='Open5GS')
]

fig.legend(
    handles=legend_patches,
    loc="upper center",
    ncol=2,
    frameon=False,
    fontsize=12
)

plt.tight_layout(rect=[0, 0, 1, 0.96])
# plt.show()
plt.savefig("fig3.png", dpi=300)
