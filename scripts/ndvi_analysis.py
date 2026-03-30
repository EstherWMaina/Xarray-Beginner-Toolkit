"""
ndvi_analysis.py
----------------
Demonstrates xarray for analyzing NDVI satellite time series
over East Africa using synthetic data modelled on MODIS MOD13A2.

Run:
    python scripts/ndvi_analysis.py

Expected output:
    - Printed dataset summaries
    - 3 saved plots: ndvi_timeseries.png, ndvi_spatial_map.png, ndvi_seasonal.png
"""

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────
# STEP 1: Generate synthetic NDVI dataset
# ─────────────────────────────────────────────

def generate_ndvi_dataset():
    """
    Creates a synthetic NDVI DataArray modelled on 16-day MODIS composites.

    NDVI (Normalized Difference Vegetation Index) ranges from -1 to 1:
        - 0.1–0.2 : bare soil, arid areas
        - 0.3–0.5 : sparse to moderate vegetation
        - 0.6–0.85: dense green vegetation (forests, croplands)

    The pattern simulates greening after the two rainy seasons.
    """
    lats = np.linspace(-5, 15, 20)
    lons = np.linspace(30, 50, 20)

    # 16-day composites for 3 years: ~68 time steps
    times = pd.date_range("2020-01-01", periods=69, freq="16D")

    np.random.seed(7)
    ndvi = np.zeros((len(times), len(lats), len(lons)))

    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Spatial baseline: highlands (western, mid-latitude) are greener
    spatial_base = (
        0.35
        + 0.008 * (lat_grid + 5)        # More green northward
        - 0.005 * (lon_grid - 30)        # More green westward (wetter)
        + 0.002 * np.random.randn(*lon_grid.shape)  # Micro-variation
    )
    spatial_base = np.clip(spatial_base, 0.1, 0.75)

    for t_idx, date in enumerate(times):
        doy = date.timetuple().tm_yday  # Day of year
        # Greenup lagging ~6 weeks behind rainfall peaks
        # Long rains green-up: peaks ~June (doy 160), Short rains: ~January (doy 15/365)
        seasonal = (
            0.20 * np.exp(-0.5 * ((doy - 160) / 30) ** 2) +   # Post-long-rains peak
            0.12 * np.exp(-0.5 * ((doy - 15) / 25) ** 2) +    # Post-short-rains peak
            0.08 * np.exp(-0.5 * ((doy - 350) / 20) ** 2)     # Dec carry-over
        )
        noise = np.random.normal(0, 0.015, (len(lats), len(lons)))
        ndvi[t_idx] = spatial_base + seasonal + noise
        ndvi[t_idx] = np.clip(ndvi[t_idx], 0.05, 0.90)

    da = xr.DataArray(
        data=ndvi,
        dims=["time", "lat", "lon"],
        coords={"time": times, "lat": lats, "lon": lons},
        name="NDVI",
        attrs={
            "units": "dimensionless",
            "long_name": "Normalized Difference Vegetation Index",
            "valid_range": "[-1, 1]",
            "source": "Synthetic data based on MODIS MOD13A2 patterns",
        }
    )
    return da


# ─────────────────────────────────────────────
# STEP 2: Explore the dataset
# ─────────────────────────────────────────────

def explore_dataset(da):
    print("=" * 55)
    print("  NDVI DATASET OVERVIEW")
    print("=" * 55)
    print(da)
    print()
    print(f"Shape        : {da.shape}")
    print(f"Time steps   : {len(da.time)} (16-day composites)")
    print(f"Date range   : {str(da.time.values[0])[:10]} → {str(da.time.values[-1])[:10]}")
    print(f"NDVI Min     : {float(da.min()):.3f}")
    print(f"NDVI Max     : {float(da.max()):.3f}")
    print(f"NDVI Mean    : {float(da.mean()):.3f}")
    print()

    # Point selection example: Nairobi-ish coordinates (~1°S, 37°E)
    nairobi_ndvi = da.sel(lat=-1.0, lon=37.0, method="nearest")
    print("  NDVI time series at Nairobi (~1°S, 37°E):")
    print(f"  Mean NDVI: {float(nairobi_ndvi.mean()):.3f}")
    print(f"  Max  NDVI: {float(nairobi_ndvi.max()):.3f}")
    print()


# ─────────────────────────────────────────────
# STEP 3: Aggregate to monthly using resample
# ─────────────────────────────────────────────

def resample_to_monthly(da):
    """
    xarray's .resample() works like pandas resample but on multi-dim arrays.
    Here we go from 16-day composites → monthly mean.
    """
    monthly = da.resample(time="MS").mean()
    print(f"Resampled to monthly: {len(monthly.time)} time steps")
    return monthly


# ─────────────────────────────────────────────
# STEP 4: Seasonal climatology for NDVI
# ─────────────────────────────────────────────

def compute_ndvi_seasonal(monthly_da):
    """Monthly climatology averaged across all pixels."""
    spatial_mean = monthly_da.mean(dim=["lat", "lon"])
    climatology = spatial_mean.groupby("time.month").mean()
    return climatology


# ─────────────────────────────────────────────
# STEP 5: Visualizations
# ─────────────────────────────────────────────

def plot_ndvi_timeseries(da):
    """
    Plot the NDVI time series at three representative pixels:
    highland, midland, lowland/arid.
    """
    # Select three representative points
    highland = da.sel(lat=10.0, lon=32.0, method="nearest")  # Ethiopian highlands
    midland  = da.sel(lat=0.0,  lon=37.0, method="nearest")  # Central Kenya
    lowland  = da.sel(lat=5.0,  lon=47.0, method="nearest")  # Somali lowland

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(da.time.values, highland.values, label="Highland (~10°N, 32°E)", color="#1b7837", linewidth=1.8)
    ax.plot(da.time.values, midland.values,  label="Midland (~0°, 37°E)",    color="#4dac26", linewidth=1.8, linestyle="--")
    ax.plot(da.time.values, lowland.values,  label="Lowland (~5°N, 47°E)",   color="#d6604d", linewidth=1.8, linestyle=":")

    ax.set_title("NDVI Time Series – Three Locations (2020–2022)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("NDVI")
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("ndvi_timeseries.png", dpi=150)
    print("  ✓ Saved: ndvi_timeseries.png")
    plt.close()


def plot_ndvi_spatial_map(da):
    """Time-mean NDVI across all time steps."""
    ndvi_mean = da.mean(dim="time")

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(
        ndvi_mean.lon, ndvi_mean.lat, ndvi_mean.values,
        cmap="RdYlGn", vmin=0.1, vmax=0.8, shading="auto"
    )
    cbar = plt.colorbar(im, ax=ax, label="Mean NDVI")
    ax.set_title("Mean NDVI (2020–2022) – East Africa", fontsize=13, fontweight="bold")
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    plt.tight_layout()
    plt.savefig("ndvi_spatial_map.png", dpi=150)
    print("  ✓ Saved: ndvi_spatial_map.png")
    plt.close()


def plot_ndvi_seasonal_cycle(climatology):
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(month_names, climatology.values, marker="o", color="#33a02c",
            linewidth=2.2, markersize=8)
    ax.fill_between(month_names, climatology.values, alpha=0.15, color="#33a02c")
    ax.set_title("NDVI Seasonal Climatology – East Africa (spatial mean)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("NDVI")
    ax.set_ylim(0.3, 0.7)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("ndvi_seasonal.png", dpi=150)
    print("  ✓ Saved: ndvi_seasonal.png")
    plt.close()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🌿 xarray NDVI Analysis — East Africa Satellite Time Series\n")

    # 1. Generate data
    ndvi_da = generate_ndvi_dataset()

    # 2. Explore
    explore_dataset(ndvi_da)

    # 3. Resample to monthly
    monthly_ndvi = resample_to_monthly(ndvi_da)

    # 4. Seasonal climatology
    climatology = compute_ndvi_seasonal(monthly_ndvi)

    # 5. Plots
    print("\nGenerating plots...")
    plot_ndvi_timeseries(ndvi_da)
    plot_ndvi_spatial_map(ndvi_da)
    plot_ndvi_seasonal_cycle(climatology)

    print("\n✅ Done! Check your working directory for the output PNG files.")