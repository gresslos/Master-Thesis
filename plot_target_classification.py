import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
import cartopy.feature as cfeature



FIGSIZE=(10,4)
FONTSIZE=14
INFOSIZE=13


# bash
# conda activate NEVARenv
# --------------------------------------------------
# 1. Read data
# --------------------------------------------------
station='Filefjell'
frame = '07883D'
file = 'ECA_EXBA_AC__TC__2B_20251017T141332Z_20251017T160711Z_07883D'

station='Tromso'
frame = '07276C'
file = 'ECA_EXBA_AC__TC__2B_20250908T134659Z_20250908T155015Z_07276C'

#station='Osteras'
#frame = '01690D'
#file = 'ECA_EXBA_AC__TC__2B_20240914T140522Z_20250906T233615Z_01690D'

#station='Filefjell'
#frame = '05160D'
#file = 'ECA_EXAC_AC__TC__2B_20250425T141414Z_20250425T160824Z_05160D'

#station='Extra'
#frame = '06518D'
#file = 'ECA_EXBA_AC__TC__2B_20250721T204913Z_20250722T000953Z_06518D'

station='Canada_Greenland'
frame = '06331C'
file = 'ECA_EXBA_AC__TC__2B_20250709T201217Z_20250709T235238Z_06331C'

station='Africa'
frame = '06497E'
file = 'ECA_EXBA_AC__TC__2B_20250720T123736Z_20250720T142320Z_06497E'

station='Africa2'
frame = '06886E'
file = 'ECA_EXBA_AC__TC__2B_20250814T123724Z_20250814T142459Z_06886E'


#path1='/xnilu_wrk2/projects/NEVAR/data/CalVal/Pyranometers/'
path1='/xnilu_wrk2/projects/NEVAR/data/EarthCARE_Real/TargetClassification/'
path2='/xnilu_wrk2/projects/NEVAR/tms/Python/figures/'
fname = f'{path1}{station}/Orbit_{frame}/{file}/{file}.h5'
fname = f'{path1}/{file}/{file}.h5'

#fname = "ECA_EXBA_AC__TC__2B_20251017T141332Z_20251017T160711Z_07883D.h5"

with h5py.File(fname, "r") as f:
    sci = f["ScienceData"]

    # Low-resolution synergetic target classification
    tc_ds = sci["synergetic_target_classification_low_resolution"]
    tc = tc_ds[...]                        # (ntime, nheight)

    # Height [m] for each bin (we use a representative vertical column)
    height = sci["height"][...]           # (ntime, nheight)
    z_center = height[0, :] / 1000.0      # km

    # Time in "seconds since 2000-01-01"
    t = sci["time"][...]                  # (ntime,)

    # Lat / lon for the top x-axis
    lat = sci["latitude"][...]
    lon = sci["longitude"][...]

    # Class definitions and colors from attributes
    defs = tc_ds.attrs["definition"].decode("utf-8")
    colors_str = tc_ds.attrs["plot_colors"].decode("utf-8")
    plot_range = tc_ds.attrs["plot_range"]

# --------------------------------------------------
# 2. Parse class labels and colors
# --------------------------------------------------
# Parse "N: label" lines into a dict {class_number: label}
class_labels = {}
for line in defs.splitlines():
    line = line.strip()
    if not line or ":" not in line:
        continue
    num_str, label = line.split(":", 1)
    class_labels[int(num_str.strip())] = label.strip()

# Hex color list (one per class index from plot_range[0]..plot_range[1])
colors = colors_str.split()
cmap = mcolors.ListedColormap(colors)
bounds = np.arange(plot_range[0] - 0.5, plot_range[1] + 1.5, 1.0)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# Only classes that actually appear in this file (keeps colorbar shorter)
classes_present = np.unique(tc)
classes_present = classes_present[(classes_present >= plot_range[0]) &
                                  (classes_present <= plot_range[1])]

# --------------------------------------------------
# 3. Build latitude and height edges for pcolormesh
# --------------------------------------------------
origin = datetime(2000, 1, 1)
dt = np.array([origin + timedelta(seconds=float(s)) for s in t])

# latitude edges
lat_edges = np.empty(lat.size + 1)
lat_edges[1:-1] = 0.5 * (lat[:-1] + lat[1:])
lat_edges[0] = lat[0] - (lat_edges[1] - lat[0])
lat_edges[-1] = lat[-1] + (lat[-1] - lat_edges[-2])

# height edges (use vertical structure from z_center)
z_edges = np.empty(z_center.size + 1)
z_edges[1:-1] = 0.5 * (z_center[:-1] + z_center[1:])
z_edges[0] = z_center[0] + (z_center[0] - z_center[1]) / 2
z_edges[-1] = z_center[-1] + (z_center[-1] - z_center[-2]) / 2

L, Z = np.meshgrid(lat_edges, z_edges)

# Transpose so shape = (nheight, ntime) for pcolormesh
tc_plot = tc.T

# --------------------------------------------------
# 4. Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE)

pc = ax.pcolormesh(L, Z, tc_plot,
                   cmap=cmap, norm=norm, shading="auto")

ax.set_ylim(0, 20)  # km
ax.set_ylabel("Altitude [km]", size=INFOSIZE)
ax.set_xlabel(r"Latitude [N$^\circ$]", fontsize=INFOSIZE)

# Extract frame ID from filename and add as text on the right
#frame_id = fname.split('_')[-1].replace('.h5', '')  # Extract "07883D"

# Title (adjust text to your liking)
date_str = dt[0].strftime("%d.%m.%Y")
#ax.set_title(f"AC-TC low resolution of synergetic target classification\n{date_str}")
# ax.set_title(f"AC-TC low resolution of synergetic target classification, {date_str}, Frame: {frame}\n")
ax.set_title(f"Target Classification (AC-TC)", fontsize=FONTSIZE)
plt.figtext(0.8, 0.0001, f"{frame} {date_str} (UTC)", fontsize=INFOSIZE*.7)    


#ax.text(1.10, 1.20, f"Frame: {frame_id}", transform=ax.transAxes, 
#        fontsize=10, ha='right', va='bottom')
# Adjust subplot to make room for colorbar on the right
plt.subplots_adjust(right=0.85)

# --------------------------------------------------
# 5.5. Add vertical dotted lines at specific latitudes for western longitudes
# --------------------------------------------------
# Find indices where latitude is approximately 68.5 and 69.5 for western longitudes
target_lats = [68.75, 69.75]
for target_lat in target_lats:
    # Find indices where latitude is close to target and longitude is negative (western side)
    lat_mask = np.abs(lat - target_lat) < 0.1  # tolerance of 0.1 degrees
    west_mask = lon < 0  # western longitudes are negative
    combined_mask = lat_mask & west_mask
    
    if np.any(combined_mask):
        # Get the best matching index (closest to target latitude)
        matching_indices = np.where(combined_mask)[0]
        lat_diffs = np.abs(lat[matching_indices] - target_lat)
        best_idx = matching_indices[np.argmin(lat_diffs)]
        
        # Draw only one vertical line per target latitude
        ax.axvline(x=lat[best_idx], color='black', linestyle=':', linewidth=1.2, alpha=0.8)

# --------------------------------------------------
# 6. Colorbar with class names
# --------------------------------------------------
# Adjust subplot to make room for colorbar on the right
#plt.subplots_adjust(right=0.85)

# Create a separate axes for the colorbar outside the plot
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="1%", pad=0.1)
cbar = fig.colorbar(pc, cax=cax)
#cbar.set_label("Synergetic target classification")

# Use only the classes that actually appear, to keep labels readable
cbar.set_ticks(classes_present)
cbar.set_ticklabels([class_labels.get(c, str(c)) for c in classes_present])
for label in cbar.ax.get_yticklabels():
    #label.set_fontsize(6)
    label.set_fontsize(INFOSIZE*0.6)

fig.tight_layout()

# Save as PNG
plt.savefig(f"github_figures/Target_Classification/target_classification_{frame}.png", dpi=300, bbox_inches='tight')

plt.show()

