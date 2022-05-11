import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

main_path = "" # write the path where the data from TrackMate is stored (.csv)

files = os.listdir(main_path)

track_id = 0
for f in files:
    if f.__contains__(".csv"):
        print(f)
        file_data = pd.read_csv(os.path.join(main_path, f))
        file_data = file_data.iloc[3:]
        file_data["TRACK_ID"] = file_data["TRACK_ID"].astype(int) + track_id
        file_data["STACK_NAME"] = len(file_data)*([str(f)])

        ids = np.unique(file_data["TRACK_ID"] )
        file_data["AREA"] = 106 * 106 * file_data["AREA"].astype(float) # Add the pixel size in nanometers
        file_data["ELLIPSE_MINOR"] = 106 * file_data["ELLIPSE_MINOR"].astype(float)
        file_data["ELLIPSE_MAJOR"] = 106 * file_data["ELLIPSE_MAJOR"].astype(float)
        file_data["ELLIPSE_ASPECTRATIO"] = file_data["ELLIPSE_ASPECTRATIO"].astype(float)
        file_data["CIRCULARITY"] = file_data["CIRCULARITY"].astype(float)
        file_data["POSITION_T"] = 2*file_data["POSITION_T"].astype(float) # Add the frame rate in minutes

        # For normalised measures, uncomment the following lines
        # ------------------------------

        for i in ids:
            cell = file_data[file_data["TRACK_ID"]==i]

            init_a = float(min(cell[cell["POSITION_T"]==min(cell["POSITION_T"])]["AREA"]))
            init_emayor = float(min(cell[cell["POSITION_T"] == min(cell["POSITION_T"])]["ELLIPSE_MAJOR"]))
            init_eminor = float(min(cell[cell["POSITION_T"] == min(cell["POSITION_T"])]["ELLIPSE_MINOR"]))
            init_aspect = float(min(cell[cell["POSITION_T"] == min(cell["POSITION_T"])]["ELLIPSE_ASPECTRATIO"]))
            init_circ = float(min(cell[cell["POSITION_T"] == min(cell["POSITION_T"])]["CIRCULARITY"]))

            file_data.loc[file_data["TRACK_ID"] == i, "AREA"] = file_data[file_data["TRACK_ID"] == i]["AREA"] / init_a
            file_data.loc[file_data["TRACK_ID"] == i, "ELLIPSE_MAJOR"] = file_data[file_data["TRACK_ID"] == i]["ELLIPSE_MAJOR"] / init_emayor
            file_data.loc[file_data["TRACK_ID"] == i, "ELLIPSE_MINOR"] = file_data[file_data["TRACK_ID"] == i]["ELLIPSE_MINOR"] / init_eminor
            file_data.loc[file_data["TRACK_ID"] == i, "ELLIPSE_ASPECTRATIO"] = file_data[file_data["TRACK_ID"] == i]["ELLIPSE_ASPECTRATIO"] / init_aspect
            file_data.loc[file_data["TRACK_ID"] == i, "CIRCULARITY"] = file_data[file_data["TRACK_ID"] == i]["CIRCULARITY"] / init_circ

        # Until here
        # ------------------------------

        if track_id == 0:
            ttrack = file_data.reset_index(drop=True)
        else:
            ttrack = pd.concat([ttrack, file_data]).reset_index(drop=True)
        track_id += max(file_data["TRACK_ID"]) + 1
del file_data



# Plot
sns.set_theme(style="white", context="paper")
# Set up the matplotlib figure
f, ([ax1, ax2], [ax3, ax4], [ax5, ax6]) = plt.subplots(3,2, figsize=(7, 5), sharex=True)
sns.lineplot(x='POSITION_T', y='AREA', palette="rocket", hue="STACK_NAME", data=ttrack, ax=ax1, legend=False)
ax1.set_ylabel("Area")
# ax1.set_ylim([0.9,1.25])
# Center the data to make it diverging
sns.lineplot(x='POSITION_T', y='ELLIPSE_MAJOR', palette="rocket", hue="STACK_NAME", ax=ax2, data=ttrack, legend=False)
ax2.set_ylabel("Major A.")
# ax2.set_ylim([0.9,1.25])
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='ELLIPSE_MINOR', palette="rocket", hue="STACK_NAME", ax=ax3, data=ttrack, legend=False)
ax3.set_ylabel("Minor A.")
# ax3.set_ylim([0.9,1.25])
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='ELLIPSE_ASPECTRATIO', palette="rocket", hue="STACK_NAME", ax=ax4, data=ttrack, legend=False)
ax4.set_ylabel("Aspect ratio")
# ax4.set_ylim([0.9,1.25])
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='CIRCULARITY', palette="rocket", hue="STACK_NAME", ax=ax5, data=ttrack, legend=False)
ax5.set_ylabel("Circularity")
ax5.set_xlabel("Time (min)")
# ax5.set_ylim([0.9,1.25])

sns.lineplot(bottom=True)
plt.xlabel("Time (min)")
plt.tight_layout(h_pad=2)

# plt.figure()
# # Randomly reorder the data to make it qualitative
# sns.scatterplot(x='AREA', y='CIRCULARITY', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)
#
# plt.figure()
# # Randomly reorder the data to make it qualitative
# sns.scatterplot(x='AREA', y='ELLIPSE_ASPECTRATIO', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)
#
# plt.figure()
# # Randomly reorder the data to make it qualitative
# sns.scatterplot(x='ELLIPSE_MAJOR', y='ELLIPSE_MINOR', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)
#
# plt.figure()
# # Randomly reorder the data to make it qualitative
# sns.scatterplot(x='AREA', y='ELLIPSE_MAJOR', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)
#
# plt.figure()
# # Randomly reorder the data to make it qualitative
# sns.scatterplot(x='ELLIPSE_MINOR', y='ELLIPSE_MAJOR', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)

fig = plt.figure(figsize=(5,5))
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='AREA', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)
plt.xlabel("Time (min)")
plt.ylabel("Area ($\mu m^2$)")
fig.savefig(os.path.join(main_path, "normalised_area.png"), format='png')


fig = plt.figure(figsize=(5,5))
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='CIRCULARITY', palette="rocket", hue="STACK_NAME", data=ttrack, legend=False)
plt.xlabel("Time (min)")
plt.ylabel("Circularity")
fig.savefig(os.path.join(main_path, "normalised_circularity.png"), format='png')

fig = plt.figure(figsize=(5,5))
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='AREA', palette="rocket", data=ttrack, legend=False)
plt.xlabel("Time (min)")
plt.ylabel("Area ($\mu m^2$)")
fig.savefig(os.path.join(main_path, "normalised_area_total.png"), format='png')


fig = plt.figure(figsize=(5,5))
# Randomly reorder the data to make it qualitative
sns.lineplot(x='POSITION_T', y='CIRCULARITY', palette="rocket", data=ttrack, legend=False)
plt.xlabel("Time (min)")
plt.ylabel("Circularity")
fig.savefig(os.path.join(main_path, "normalised_circularity_total.png"), format='png')



