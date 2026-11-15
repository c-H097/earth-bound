#  LDRM_80S_1000MPP_ADJ_SLP_100M.TIF    https://pgda.gsfc.nasa.gov/data/LOLA_20mpp/LDRM_80S_1000MPP_ADJ_SLP_100M.TIF
#    LDRM_80S_1000MPP_ADJ_ROUGH_100M.TIF      https://pgda.gsfc.nasa.gov/data/LOLA_20mpp/LDRM_80S_1000MPP_ADJ_ROUGH_100M.TIF

import rasterio
from rasterio.windows import from_bounds
import numpy as np

# --- 1. Paste your URLs here ---
slope_url = r"C:\Users\Mariam\Downloads\LDRM_80S_1000MPP_ADJ_SLP_100M.tiff"  
rough_url = r"C:\Users\Mariam\Downloads\LDRM_80S_1000MPP_ADJ_ROUGH_100M.tiff"

# --- 2. Define your Area of Interest (in meters, same projection as file) ---
# Example: A 100km x 100km box around the pole. ADJUST THESE.
x_min, x_max = -50000, 50000
y_min, y_max = -50000, 50000

def get_stats_from_remote_cog(url, bounds, name):
    print(f"--- Reading {name} ---")
    # Open the remote file (this only downloads the header, not the data)
    with rasterio.open(url) as src:
        # Create a window from your geographic bounds
        window = from_bounds(x_min, y_min, x_max, y_max, src.transform)
        
        # Read ONLY that window of data
        data = src.read(1, window=window)
        
        # Filter out NoData values (LOLA often uses very negative numbers or zeros)
        # For slope, valid values are 0-90. For roughness, valid values > 0.
        if name == "Slope":
            valid_data = data[(data >= 0) & (data <= 90)]
        else: # Roughness
            valid_data = data[data > 0]
            
        if valid_data.size == 0:
            print("No valid data found in this window. Try a different bounding box.")
            return None
            
        median_val = np.median(valid_data)
        print(f"Median {name}: {median_val:.2f}")
        return median_val

# Run the function for both files
median_slope = get_stats_from_remote_cog(slope_url, (x_min, y_min, x_max, y_max), "Slope")
median_rough = get_stats_from_remote_cog(rough_url, (x_min, y_min, x_max, y_max), "Roughness")

# --- 4. Convert to the app's 0-100 index ---
if median_slope is not None:
    # Simple linear mapping: 30 degrees = 100
    slope_index = (median_slope / 30.0) * 100
    print(f"\nApp Slope Index (0-100): {slope_index:.1f}")

if median_rough is not None:
    # Simple linear mapping: 10 meters = 100
    rough_index = (median_rough / 10.0) * 100
    print(f"App Roughness Index (0-100): {rough_index:.1f}")