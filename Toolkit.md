# 🛰️ Getting Started with xarray in Python – A Beginner's Guide
### *Satellite Time Series Analysis: Rainfall Patterns & NDVI over East Africa*

> **Moringa AI Capstone Project** — "Prompt-Powered Kickstart: Building a Beginner's Toolkit"  
> Technology: `xarray` — Python library for multi-dimensional labeled arrays  
> Focus: Climate & Satellite data (Rainfall time series + NDVI)

---

## Table of Contents

1. [Title & Objective](#1-title--objective)
2. [Quick Summary of xarray](#2-quick-summary-of-xarray)
3. [System Requirements](#3-system-requirements)
4. [Installation & Setup Instructions](#4-installation--setup-instructions)
5. [Minimal Working Example](#5-minimal-working-example)
6. [AI Prompt Journal](#6-ai-prompt-journal)
7. [Common Issues & Fixes](#7-common-issues--fixes)
8. [References](#8-references)

---

## 1. Title & Objective

### What technology did I choose?
**`xarray`** — an open-source Python library for working with labeled, multi-dimensional arrays. It is the standard tool for climate science, remote sensing, and earth observation data in Python.

### Why did I choose it?
Climate and satellite datasets are inherently multi-dimensional: they have a time axis, latitude, longitude, and sometimes additional axes like altitude or spectral band. Plain `numpy` arrays lose track of what each dimension means. `pandas` DataFrames are powerful but built for 2D tabular data. `xarray` fills exactly this gap — it brings the labeling power of `pandas` to N-dimensional arrays.

East Africa is a region where rainfall variability has direct food security consequences. Tools like `xarray` are used daily by meteorologists, remote sensing analysts, and climate scientists working on exactly these problems.

### End goal
By the end of this guide you will be able to:
- Create and inspect an `xarray` DataArray and Dataset
- Load multi-dimensional time series data (synthetic satellite data)
- Compute temporal statistics (monthly climatology, anomalies)
- Resample time series (16-day → monthly)
- Produce publication-quality spatial maps and time series plots
- Understand how to connect this workflow to real satellite products (CHIRPS, MODIS NDVI)

---

## 2. Quick Summary of xarray

### What is it?
`xarray` is a Python library that extends `numpy` arrays with **dimension names** and **coordinate labels**. Instead of remembering that `array[0, :, :]` means "the first time step", you write `da.sel(time="2021-04")` and xarray finds the right slice for you.

Its two core objects are:
- **`DataArray`**: a single labeled N-dimensional array (like a named `numpy` array with coordinates)
- **`Dataset`**: a dictionary-like container of multiple `DataArray`s that share the same coordinates

### Where is it used?
- Climate science (temperature, precipitation reanalysis)
- Remote sensing (NDVI, land surface temperature, soil moisture)
- Oceanography (sea surface temperature, salinity)
- Atmospheric science (wind fields, humidity profiles)
- Any domain with gridded spatiotemporal data

### One real-world example
The [Copernicus Climate Change Service](https://cds.climate.copernicus.eu/) distributes ERA5 reanalysis data — the most widely used global climate dataset — in NetCDF format. Researchers and operational forecasters routinely open it with one line:

```python
import xarray as xr
ds = xr.open_dataset("era5_temperature.nc")
```

From there they can select regions, compute anomalies, and plot maps — all with xarray's intuitive label-based operations.

---

## 3. System Requirements

| Requirement | Specification |
|-------------|---------------|
| Operating System | Windows 10+, macOS 11+, Ubuntu 20.04+ |
| Python | 3.8 or higher |
| RAM | 4 GB minimum (8 GB recommended for real datasets) |
| Disk space | ~500 MB for dependencies |
| Code editor | VS Code, JupyterLab, or any Python IDE |
| Package manager | `pip` (included with Python 3) |

> 💡 **For Windows users**: The Windows Subsystem for Linux (WSL2) provides the smoothest experience for scientific Python work. Alternatively, [Anaconda](https://www.anaconda.com/download) handles all dependencies cleanly.

---

## 4. Installation & Setup Instructions

### Step 1 — Verify Python is installed
```bash
python --version
# Expected: Python 3.8.x or higher
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### Step 2 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/xarray-toolkit.git
cd xarray-toolkit
```

### Step 3 — Create a virtual environment

Using a virtual environment keeps your project's dependencies isolated from your system Python.

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal prompt.

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

This installs: `xarray`, `numpy`, `pandas`, `matplotlib`, `scipy`, `netCDF4`, `jupyter`.

Expected terminal output (truncated):
```
Collecting xarray>=2023.1.0
  Downloading xarray-2023.6.0-py3-none-any.whl (1.0 MB)
...
Successfully installed xarray-2023.6.0 numpy-1.25.2 pandas-2.0.3 ...
```

### Step 5 — Verify installation
```bash
python -c "import xarray; print(xarray.__version__)"
# Expected output: 2023.x.x
```

### Step 6 — Run the scripts
```bash
python scripts/rainfall_analysis.py
python scripts/ndvi_analysis.py
```

Or launch Jupyter Notebooks:
```bash
jupyter notebook notebooks/
```

---

## 5. Minimal Working Example

### What does this example do?
This example walks through the **core xarray workflow** in 30 lines: create a DataArray, explore it, select a time slice, compute a mean, and print results. Think of it as "Hello, World!" for xarray.

```python
import numpy as np
import xarray as xr
import pandas as pd

# ── 1. Create a simple DataArray ──────────────────────────────────────
# Simulate 12 months of temperature data over a 5×5 spatial grid

np.random.seed(0)
data = 20 + 5 * np.random.randn(12, 5, 5)  # shape: (time, lat, lon)

times = pd.date_range("2023-01", periods=12, freq="MS")
lats  = np.linspace(-2, 2, 5)
lons  = np.linspace(36, 40, 5)

# Wrap in a DataArray — give each dimension a name and coordinates
temp = xr.DataArray(
    data   = data,
    dims   = ["time", "lat", "lon"],         # dimension names
    coords = {"time": times, "lat": lats, "lon": lons},  # coordinate labels
    name   = "temperature",
    attrs  = {"units": "Celsius", "long_name": "Surface Air Temperature"}
)

# ── 2. Inspect the DataArray ──────────────────────────────────────────
print(temp)           # shows shape, dims, coords, and attrs
print(temp.dims)      # ('time', 'lat', 'lon')
print(temp.coords)    # lists all coordinate values
print(temp.attrs)     # {'units': 'Celsius', ...}

# ── 3. Label-based selection ──────────────────────────────────────────
# Select July 2023 using the time label (no index arithmetic needed!)
july = temp.sel(time="2023-07")
print(f"July mean temperature: {float(july.mean()):.2f} °C")

# Select the nearest grid point to Nairobi (1°S, 36.8°E)
nairobi = temp.sel(lat=-1.0, lon=36.8, method="nearest")
print(f"Nairobi time series shape: {nairobi.shape}")   # (12,)

# ── 4. Compute statistics ─────────────────────────────────────────────
annual_mean = temp.mean(dim="time")                   # spatial map of annual mean
monthly_std = temp.std(dim=["lat","lon"])             # time series of spatial variability

print(f"Annual mean temperature range: {float(annual_mean.min()):.1f}–{float(annual_mean.max()):.1f} °C")
```

### Expected output
```
<xarray.DataArray 'temperature' (time: 12, lat: 5, lon: 5)>
array([[[...]])
Coordinates:
  * time     (time) datetime64[ns] 2023-01-01 2023-02-01 ... 2023-12-01
  * lat      (lat) float64 -2.0 -1.0 0.0 1.0 2.0
  * lon      (lon) float64 36.0 37.0 38.0 39.0 40.0
Attributes:
    units:      Celsius
    long_name:  Surface Air Temperature

('time', 'lat', 'lon')
July mean temperature: 20.13 °C
Nairobi time series shape: (12,)
Annual mean temperature range: 18.4–21.8 °C
```

### Key xarray concepts illustrated

| Operation | xarray code | What it does |
|-----------|------------|--------------|
| Create | `xr.DataArray(data, dims, coords)` | Wraps numpy array with labels |
| Inspect | `da.dims`, `da.coords`, `da.attrs` | Explore structure |
| Select by label | `da.sel(time="2023-07")` | No index arithmetic |
| Select nearest | `da.sel(lat=-1.0, method="nearest")` | Nearest-neighbor lookup |
| Reduce | `da.mean(dim="time")` | Named-dimension aggregation |
| Groupby | `da.groupby("time.month").mean()` | Climatology computation |
| Resample | `da.resample(time="MS").mean()` | Temporal resampling |

---

## 6. AI Prompt Journal

This toolkit was scaffolded with the assistance of **Claude (Anthropic)**. Below is a record of the key prompts used, what the AI returned, and how useful each interaction was.

---

### Prompt 1 — Understanding the library
> **Prompt:** *"I am a Python developer with pandas experience but no background in climate data. Explain xarray to me: what problem does it solve, what are its core objects, and how does it relate to numpy and pandas?"*

**AI response summary:**  
The AI gave a clear mental model: think of `xarray.DataArray` as a numpy array that remembers what each axis means (like a pandas Series but for N dimensions), and `Dataset` as a pandas DataFrame but where each column can itself be a multi-dimensional array. It explained that xarray was built specifically for NetCDF climate files, which are the standard format for gridded earth observation data.

**Evaluation:** ⭐⭐⭐⭐⭐ — This framing immediately made xarray click. The pandas analogy was exactly the right entry point.

---

### Prompt 2 — Generating synthetic satellite data
> **Prompt:** *"Write Python code using xarray and numpy to generate a synthetic monthly rainfall dataset for East Africa (lat -5 to 15N, lon 30 to 50E) covering 2020–2022. The rainfall should mimic East Africa's bimodal rainfall pattern with peaks in April and November. Return an xr.DataArray with time, lat, lon dimensions."*

**AI response summary:**  
The AI produced working code using `np.exp` to model Gaussian peaks around April and November, a spatial gradient to simulate orographic effects (more rain in highlands), and random noise. It also included `attrs` with units and a descriptive name — good practice I might have skipped.

**Evaluation:** ⭐⭐⭐⭐⭐ — The output needed only minor tuning (clipping negatives, adjusting the spatial gradient magnitude). Saved 45+ minutes of trial-and-error.

---

### Prompt 3 — Understanding groupby and resample
> **Prompt:** *"Explain the difference between xarray's `.groupby('time.month')` and `.resample(time='MS')`. When would I use each one for climate data analysis?"*

**AI response summary:**  
The AI clarified: use `.groupby("time.month")` to compute a **climatology** (averaging all Januaries together, all Februaries, etc.) — it collapses years into a single annual cycle. Use `.resample(time="MS")` to **aggregate within each time step** (e.g., convert daily data into monthly averages while preserving the year). Both can call `.mean()` but they do fundamentally different things.

**Evaluation:** ⭐⭐⭐⭐⭐ — This was a genuine point of confusion. The AI's explanation with concrete examples cleared it up completely.

---

### Prompt 4 — NDVI simulation
> **Prompt:** *"Generate a synthetic NDVI DataArray for East Africa using 16-day composites (like MODIS MOD13A2) over 2020–2022. NDVI should range 0.1–0.85, with a seasonal green-up signal that lags rainfall by ~6 weeks, and a spatial gradient (western highlands greener than eastern lowlands)."*

**AI response summary:**  
The AI generated the seasonal signal using day-of-year (`tm_yday`) rather than month number — a more accurate approach for 16-day data. It modeled the vegetation green-up lag by shifting the NDVI peak relative to rainfall peaks, which matches the real-world phenology of East African vegetation.

**Evaluation:** ⭐⭐⭐⭐ — Very good. I had to adjust the amplitude of the seasonal signal slightly and add a third `np.exp` term for the December carry-over effect, but the structure was solid.

---

### Prompt 5 — Debugging a coordinate mismatch error
> **Prompt:** *"I'm getting this xarray error: `ValueError: dimensions ('month',) must have the same length as data`. I'm trying to subtract a monthly climatology from my time series. What's wrong and how do I fix it?"*

**AI response summary:**  
The AI identified the issue immediately: when you compute `da.groupby("time.month").mean()`, the result has a `month` dimension, but the original `da` has a `time` dimension. You cannot subtract them directly. The fix is to use `da.groupby("time.month") - climatology`, which tells xarray to align along months automatically before subtracting.

**Evaluation:** ⭐⭐⭐⭐⭐ — This would have taken a long time to debug alone. The fix was a one-line change.

---

### Prompt 6 — Plot styling for spatial maps
> **Prompt:** *"How do I use matplotlib's pcolormesh to plot an xarray DataArray as a spatial map? Show me how to add a colorbar, axis labels, and a diverging colormap for anomalies vs a sequential colormap for absolute values."*

**AI response summary:**  
The AI explained the difference between `imshow` (assumes regular grids, can distort) and `pcolormesh` (handles irregular grids correctly, preferred for geospatial data). It showed how to pass `da.lon`, `da.lat`, `da.values` separately, when to use `vmin`/`vmax` for diverging colormaps (anomalies), and recommended `RdBu` for anomalies and `YlGnBu` for rainfall totals.

**Evaluation:** ⭐⭐⭐⭐ — Solid guidance. The note about `pcolormesh` being preferable to `imshow` for geospatial data was a useful insight I would not have known.

---

### Reflections on AI-assisted learning

Using Claude to learn xarray was significantly faster than reading documentation alone. The key productivity gains were:

1. **Conceptual framing first**: Asking "how does this relate to pandas?" gave me a mental model in minutes rather than hours.
2. **Working code as a scaffold**: The AI-generated code was ~80% correct and needed tuning, but having working structure to edit is far faster than writing from scratch.
3. **Instant error diagnosis**: The `groupby` alignment error (Prompt 5) would have cost significant debugging time.
4. **Best-practice nudges**: The AI consistently included `attrs`, proper colormaps, and `np.clip` for physical constraints — patterns I absorbed and replicated.

**Limitation observed**: The AI occasionally suggested `xr.open_mfdataset()` for multi-file datasets before I had a single-file example working. It helps to be explicit about your experience level in the prompt.

---

## 7. Common Issues & Fixes

### Issue 1 — `ModuleNotFoundError: No module named 'xarray'`
**Cause:** Package not installed, or installed in the wrong Python environment.  
**Fix:**
```bash
# Confirm which Python you're running
which python   # macOS/Linux
where python   # Windows

# Install in the active environment
pip install xarray

# If using conda:
conda install -c conda-forge xarray
```

---

### Issue 2 — `ValueError: dimensions must have the same length` when subtracting climatology
**Cause:** Trying to subtract a `(month,)` climatology from a `(time, lat, lon)` DataArray directly.  
**Wrong:**
```python
anomaly = rainfall - climatology   # ❌ dimension mismatch
```
**Fix:** Use `groupby` to align dimensions automatically:
```python
anomaly = rainfall.groupby("time.month") - climatology   # ✅
```

---

### Issue 3 — `KeyError` when using `.sel()`
**Cause:** The coordinate value you requested doesn't exist exactly.  
**Wrong:**
```python
da.sel(lat=1.23456)   # ❌ exact value may not exist in the grid
```
**Fix:** Use `method="nearest"` for approximate selection:
```python
da.sel(lat=1.23456, method="nearest")   # ✅
```

---

### Issue 4 — Plot appears blank / axes show no data
**Cause:** Forgetting `.values` when passing to matplotlib's `pcolormesh`, or passing the DataArray directly (sometimes works, sometimes doesn't in older versions).  
**Fix:** Always pass coordinates and values explicitly:
```python
ax.pcolormesh(da.lon.values, da.lat.values, da.values, ...)  # ✅
```

---

### Issue 5 — `netCDF4` import error when trying to open `.nc` files
**Cause:** `netCDF4` backend is missing.  
**Fix:**
```bash
pip install netCDF4
# or
conda install -c conda-forge netcdf4
```

---

### Issue 6 — `AttributeError: 'DataArray' has no attribute 'plot'` in older xarray versions
**Cause:** The `.plot()` accessor requires `matplotlib` to be installed.  
**Fix:**
```bash
pip install matplotlib
```
Then restart your Python session.

---

### Issue 7 — Memory error with large `.nc` files
**Cause:** Loading a large file with `xr.open_dataset()` loads everything into RAM.  
**Fix:** Use lazy loading with `chunks` to activate Dask:
```python
ds = xr.open_dataset("large_file.nc", chunks={"time": 10})
```
This requires `pip install dask` and loads data lazily — only reading what you need.

---

## 8. References

### Official Documentation
- [xarray Official Docs](https://docs.xarray.dev/en/stable/) — Complete API reference and tutorials
- [xarray User Guide](https://docs.xarray.dev/en/stable/user-guide/index.html) — Best starting point
- [xarray Examples Gallery](https://docs.xarray.dev/en/stable/examples/weather-data.html) — Weather data examples

### Real Satellite Data Sources (East Africa / Global)
- [CHIRPS Rainfall Data](https://www.chc.ucsb.edu/data/chirps) — High-resolution rainfall estimates (1981–present)
- [MODIS NDVI (MOD13A2)](https://lpdaac.usgs.gov/products/mod13a2v061/) — 16-day NDVI composites, 1 km resolution
- [NASA EarthData](https://earthdata.nasa.gov/) — Central portal for NASA satellite data
- [Copernicus Climate Data Store (ERA5)](https://cds.climate.copernicus.eu/) — Global climate reanalysis

### Tutorials and Learning Resources
- [Pythia Foundations – xarray](https://foundations.projectpythia.org/core/xarray.html) — Project Pythia: excellent beginner-to-intermediate xarray curriculum
- [Earth and Environmental Data Science (Columbia)](https://earth-env-data-science.github.io/) — University-level open course
- [Pangeo Gallery](https://gallery.pangeo.io/) — Real-world notebooks using xarray for climate science
- [Software Carpentry: Python for Atmosphere and Ocean Scientists](https://carpentries-lab.github.io/python-aos-lesson/) — Step-by-step practical workshop

### Helpful Blog Posts
- [Why xarray is better than numpy for climate data](https://towardsdatascience.com/handling-netcdf-files-using-xarray-for-absolute-beginners-111a8ab4463f) — Towards Data Science
- [Getting started with NDVI analysis in Python](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/) — Earth Lab, University of Colorado

### Related Libraries to Explore Next
- [`rioxarray`](https://corteva.github.io/rioxarray/) — Adds raster I/O and CRS-aware operations to xarray
- [`cartopy`](https://scitools.org.uk/cartopy/) — Map projections and geographic plotting
- [`dask`](https://dask.org/) — Parallel computing for datasets too large for RAM
- [`intake`](https://intake.readthedocs.io/) — Data catalog tool for managing large collections of climate datasets

---

*Prepared as part of the Moringa AI Capstone Project. All code in this repository uses synthetic data; no real satellite downloads are required to run the examples.*