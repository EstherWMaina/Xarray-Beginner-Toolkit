"""
rainfall_analysis.py
--------------------
Demonstrates xarray for analyzing satellite-derived rainfall time series
over East Africa using synthetic data.

Run:
    python scripts/rainfall_analysis.py

Expected output:
    - Printed dataset summaries and statistics
    - 3 saved plots: seasonal_cycle.png, spatial_mean_rainfall.png, anomaly_map.png
"""

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ─────────────────────────────────────────────
# STEP 1: Generate synthetic rainfall dataset
# ─────────────────────────────────────────────

def generate_rainfall_dataset():
    """
    Creates a synthetic monthly rainfall DataArray mimicking
    East Africa's bimodal rainfall pattern (long rains: Mar-May,
    short rains: Oct-Dec).
    """
    # Define spatial coordinates (East Africa bounding box)
    lats = np.linspace(-5, 15, 20)   # 20 latitude steps
    lons = np.linspace(30, 50, 20)   # 20 longitude steps

    # Define time: monthly from Jan 2020 to Dec 2022
    times = pd.date_range("2020-01", periods=36, freq="MS")

    # Build rainfall values with:
    # - Bimodal seasonal cycle (two peaks per year)
    # - Spatial gradient (more rain in highlands/western areas)
    # - Random noise to mimic real variability
    np.random.seed(42)

    rainfall = np.zeros((len(times), len(lats), len(lons)))

    for t_idx, date in enumerate(times):
        month = date.month
        # Bimodal seasonal signal: peaks in April and November
        seasonal = (
            6 * np.exp(-0.5 * ((month - 4) / 1.5) ** 2) +   # Long rains peak
            4 * np.exp(-0.5 * ((month - 11) / 1.5) ** 2)    # Short rains peak
        )
        # Spatial gradient: more rain at higher latitudes (north) & western lons
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        spatial = 1.0 + 0.03 * (lat_grid + 5) - 0.01 * (lon_grid - 30)
        # Combine and add noise
        rainfall[t_idx] = seasonal * spatial + np.random.normal(0, 0.5, (len(lats), len(lons)))
        rainfall[t_idx] = np.clip(rainfall[t_idx], 0, None)  # No negative rainfall

    # Wrap in an xarray DataArray
    da = xr.DataArray(
        data=rainfall,
        dims=["time", "lat", "lon"],
        coords={"time": times, "lat": lats, "lon": lons},
        name="rainfall",
        attrs={
            "units": "mm/day",
            "long_name": "Monthly Mean Rainfall",
            "source": "Synthetic data (East Africa pattern)",
        }
    )
    return da


# ─────────────────────────────────────────────
# STEP 2: Explore the dataset
# ─────────────────────────────────────────────

def explore_dataset(da):
    print("=" * 55)
    print("  RAINFALL DATASET OVERVIEW")
    print("=" * 55)
    print(da)
    print()
    print(f"Shape     : {da.shape}")
    print(f"Dimensions: {dict(da.dims)}")
    print(f"Min value : {float(da.min()):.2f} mm/day")
    print(f"Max value : {float(da.max()):.2f} mm/day")
    print(f"Mean      : {float(da.mean()):.2f} mm/day")
    print()


# ─────────────────────────────────────────────
# STEP 3: Compute seasonal cycle
# ─────────────────────────────────────────────

def compute_seasonal_cycle(da):
    """
    Average rainfall by month across all years and locations.
    xarray's .groupby("time.month").mean() makes this very clean.
    """
    # Spatial mean first (average over lat and lon)
    spatial_mean = da.mean(dim=["lat", "lon"])

    # Then group by calendar month and average across all years
    monthly_climatology = spatial_mean.groupby("time.month").mean()

    print("Monthly climatology (mm/day):")
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    for m, val in zip(month_names, monthly_climatology.values):
        bar = "█" * int(val * 3)
        print(f"  {m}: {val:.2f}  {bar}")
    print()
    return monthly_climatology


# ─────────────────────────────────────────────
# STEP 4: Compute anomalies
# ─────────────────────────────────────────────

def compute_anomalies(da):
    """
    Rainfall anomaly = actual value minus the climatological mean for that month.
    This highlights wet/dry years relative to the average.
    """
    climatology = da.groupby("time.month").mean("time")
    anomaly = da.groupby("time.month") - climatology
    anomaly.attrs["units"] = "mm/day"
    anomaly.attrs["long_name"] = "Rainfall Anomaly"
    return anomaly


# ─────────────────────────────────────────────
# STEP 5: Visualizations
# ─────────────────────────────────────────────

def plot_seasonal_cycle(monthly_climatology):
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(month_names, monthly_climatology.values, color="#2196F3", edgecolor="white", linewidth=0.8)
    ax.set_title("East Africa – Monthly Rainfall Climatology", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Rainfall (mm/day)")
    ax.axhline(monthly_climatology.mean(), color="red", linestyle="--", label="Annual mean")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("seasonal_cycle.png", dpi=150)
    print("  ✓ Saved: seasonal_cycle.png")
    plt.close()


def plot_spatial_mean_rainfall(da):
    """Time-mean rainfall map — average across all 36 months."""
    time_mean = da.mean(dim="time")
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(
        time_mean.lon, time_mean.lat, time_mean.values,
        cmap="YlGnBu", shading="auto"
    )
    cbar = plt.colorbar(im, ax=ax, label="Rainfall (mm/day)")
    ax.set_title("3-Year Mean Rainfall (2020–2022)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    plt.tight_layout()
    plt.savefig("spatial_mean_rainfall.png", dpi=150)
    print("  ✓ Saved: spatial_mean_rainfall.png")
    plt.close()


def plot_anomaly_map(anomaly):
    """Plot the rainfall anomaly for April 2021 (peak long rains)."""
    # Select April 2021
    april_2021 = anomaly.sel(time="2021-04")
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(
        april_2021.lon, april_2021.lat, april_2021.values,
        cmap="RdBu", vmin=-3, vmax=3, shading="auto"
    )
    cbar = plt.colorbar(im, ax=ax, label="Anomaly (mm/day)")
    ax.set_title("Rainfall Anomaly – April 2021 (Long Rains)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    plt.tight_layout()
    plt.savefig("anomaly_map.png", dpi=150)
    print("  ✓ Saved: anomaly_map.png")
    plt.close()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🛰️  xarray Rainfall Analysis — East Africa\n")

    # 1. Generate data
    rainfall_da = generate_rainfall_dataset()

    # 2. Explore
    explore_dataset(rainfall_da)

    # 3. Seasonal cycle
    climatology = compute_seasonal_cycle(rainfall_da)

    # 4. Anomalies
    anomaly = compute_anomalies(rainfall_da)

    # 5. Plots
    print("Generating plots...")
    plot_seasonal_cycle(climatology)
    plot_spatial_mean_rainfall(rainfall_da)
    plot_anomaly_map(anomaly)

    print("\n✅ Done! Check your working directory for the output PNG files.")