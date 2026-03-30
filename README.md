# 🛰️ Getting Started with xarray in Python – A Beginner's Guide
### *Satellite Time Series Analysis: Rainfall Patterns & NDVI over East Africa*

> **Moringa AI Capstone Project** — "Prompt-Powered Kickstart: Building a Beginner's Toolkit"

---

## Table of Contents

1. [Title & Objective](#1-title--objective)
2. [Quick Summary of the Technology](#2-quick-summary-of-the-technology)
3. [System Requirements](#3-system-requirements)
4. [Installation & Setup Instructions](#4-installation--setup-instructions)
5. [Minimal Working Example](#5-minimal-working-example)
6. [AI Prompt Journal](#6-ai-prompt-journal)
7. [Common Issues & Fixes](#7-common-issues--fixes)
8. [References](#8-references)

---

## 1. Title & Objective

**Getting Started with xarray in Python – Satellite Time Series for Rainfall & NDVI**

### What technology did I choose?
**`xarray`** — an open-source Python library for working with labeled, multi-dimensional arrays. It is the standard tool in climate science, remote sensing, and earth observation data analysis.

### Why did I choose it?
Climate and satellite datasets are inherently multi-dimensional: they have a time axis, latitude, longitude, and sometimes additional axes like altitude or spectral band. Plain `numpy` arrays lose track of what each dimension means, and `pandas` DataFrames are built for 2D tabular data. `xarray` fills exactly this gap — it brings the labeling power of `pandas` to N-dimensional arrays.

East Africa is a region where rainfall variability has direct food security consequences. Tools like `xarray` are used daily by meteorologists, remote sensing analysts, and climate scientists working on exactly these problems — making it a practical and meaningful choice.

### What's the end goal?
By the end of this guide you will be able to:
- Create and inspect `xarray` `DataArray` and `Dataset` objects
- Analyze multi-dimensional satellite time series (rainfall + NDVI)
- Compute temporal statistics: monthly climatology and anomalies
- Resample time series from 16-day composites to monthly averages
- Produce spatial maps and time series plots using `matplotlib`

---

## 2. Quick Summary of the Technology

> *"xarray is an open-source Python library that makes working with labeled, multi-dimensional arrays simple, efficient, and intuitive."*

### What is it?
`xarray` extends `numpy` arrays with **dimension names** and **coordinate labels**. Instead of remembering that `array[0, :, :]` means "the first time step", you write `da.sel(time="2021-04")` and xarray finds the right slice for you.

Its two core objects are:
- **`DataArray`** — a single labeled N-dimensional array (think: a named `numpy` array with coordinates)
- **`Dataset`** — a dictionary-like container of multiple `DataArray`s sharing the same coordinates

### Where is it used?
- Climate science (temperature, precipitation reanalysis)
- Remote sensing (NDVI, land surface temperature, soil moisture)
- Oceanography (sea surface temperature, salinity profiles)
- Atmospheric science (wind fields, humidity)
- Any domain with gridded spatiotemporal data

### One real-world example
The [Copernicus Climate Change Service](https://cds.climate.copernicus.eu/) distributes **ERA5** — the most widely used global climate reanalysis dataset — in NetCDF format. Researchers and operational forecasters open it with a single line:

```python
import xarray as xr
ds = xr.open_dataset("era5_temperature.nc")
```

From there they select regions, compute anomalies, and generate maps — all using xarray's intuitive label-based operations.

---

## 3. System Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 10+, macOS 11+, Ubuntu 20.04+ |
| **Python** | 3.8 or higher |
| **Editor** | VS Code, JupyterLab, or any Python IDE |
| **RAM** | 4 GB minimum (8 GB recommended for real datasets) |
| **Disk space** | ~500 MB for all dependencies |
| **Package manager** | `pip` (included with Python 3) |

> 💡 **Windows users**: [Anaconda](https://www.anaconda.com/download) handles all scientific Python dependencies cleanly and is the recommended option on Windows.

---

## 4. Installation & Setup Instructions

### Step 1 — Verify Python is installed
```bash
python --version
# Expected: Python 3.8.x or higher
```
If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### Step 2 — Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/xarray-toolkit.git
cd xarray-toolkit
```

### Step 3 — Create a virtual environment
A virtual environment keeps project dependencies isolated from your system Python.

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

Expected output (truncated):
```
Collecting xarray>=2023.1.0
  Downloading xarray-2023.6.0-py3-none-any.whl (1.0 MB)
...
Successfully installed xarray-2023.6.0 numpy-1.25.2 pandas-2.0.3 matplotlib-3.7.2 ...
```

### Step 5 — Verify the installation
```bash
python -c "import xarray; print(xarray.__version__)"
# Expected: 2023.x.x
```

### Step 6 — Run the scripts
```bash
# Rainfall pattern analysis → saves 3 PNG plots
python scripts/rainfall_analysis.py

# NDVI satellite time series → saves 3 PNG plots
python scripts/ndvi_analysis.py
```

### Step 7 — Or explore the Jupyter Notebooks
```bash
jupyter notebook notebooks/
```
Open the notebooks in order: `01_xarray_basics` → `02_rainfall_timeseries` → `03_ndvi_analysis`.

---

## 5. Minimal Working Example

### What does this example do?
Creates a simple temperature `DataArray`, selects data by label, and computes a spatial mean — the three most fundamental xarray operations.

```python
import numpy as np
import xarray as xr
import pandas as pd

# 1. Create a DataArray — a numpy array with named dimensions and coordinate labels
data  = 20 + 5 * np.random.randn(12, 5, 5)           # shape: (time, lat, lon)
times = pd.date_range("2023-01", periods=12, freq="MS")
lats  = np.linspace(-2, 2, 5)
lons  = np.linspace(36, 40, 5)

temp = xr.DataArray(
    data   = data,
    dims   = ["time", "lat", "lon"],                   # name each axis
    coords = {"time": times, "lat": lats, "lon": lons},
    name   = "temperature",
    attrs  = {"units": "Celsius"}                      # attach metadata
)

# 2. Select by label — no index arithmetic needed
july = temp.sel(time="2023-07")
print(f"July mean: {float(july.mean()):.2f} °C")

# 3. Select nearest grid point to Nairobi (~1°S, 36.8°E)
nairobi = temp.sel(lat=-1.0, lon=36.8, method="nearest")
print(f"Nairobi series shape: {nairobi.shape}")        # (12,) — one value per month

# 4. Reduce along a named dimension
annual_mean = temp.mean(dim="time")                    # spatial map of annual mean
print(f"Annual mean shape: {annual_mean.shape}")       # (5, 5)
```

### Expected output
```
July mean: 20.13 °C
Nairobi series shape: (12,)
Annual mean shape: (5, 5)
```

---

## 6. AI Prompt Journal

This toolkit was built with the assistance of **Claude (Anthropic)**. Below are the key prompts used during development.

---

**Prompt 1 — Understanding xarray**
> *"I have pandas experience but no background in climate data. Explain xarray to me: what problem does it solve, what are its core objects, and how does it relate to numpy and pandas?"*

<<<<<<< HEAD
**Response summary:** The AI framed `DataArray` as a numpy array that remembers what each axis means — like a pandas Series but for N dimensions. It explained xarray was built specifically for NetCDF climate files, the standard format for gridded earth observation data.

**Helpfulness:** ⭐⭐⭐⭐⭐ — The pandas analogy made xarray click immediately and saved a lot of doc-reading time.
=======
This entire toolkit was scaffolded using **Claude (Anthropic)**. The `TOOLKIT.md` document includes a full **AI Prompt Journal** showing which prompts were used, what the AI returned, and how it accelerated learning. See [TOOLKIT.md](https://github.com/EstherWMaina/Xarray-Beginner-Toolkit/blob/main/Toolkit.md).
>>>>>>> c6df480d5beb50cc7b5eefde1fc47f4a42e1b551

---

**Prompt 2 — Generating synthetic East Africa rainfall data**
> *"Write Python code using xarray and numpy to generate a synthetic monthly rainfall dataset for East Africa (lat -5 to 15N, lon 30 to 50E) for 2020–2022, mimicking the bimodal rainfall pattern with peaks in April and November."*

**Response summary:** The AI used `np.exp` Gaussian peaks to model the two rainy seasons and included a spatial gradient for orographic effects. It also added `attrs` with units — a best practice I would have skipped initially.

**Helpfulness:** ⭐⭐⭐⭐⭐ — Output needed minor tuning but saved significant trial-and-error time.

---

**Prompt 3 — groupby vs resample**
> *"Explain the difference between xarray's `.groupby('time.month')` and `.resample(time='MS')`. When would I use each one for climate data analysis?"*

**Response summary:** Use `.groupby("time.month")` to compute a climatology — averaging all Januaries together across years. Use `.resample(time="MS")` to aggregate within each month while preserving the year (e.g. converting 16-day NDVI composites to monthly averages).

**Helpfulness:** ⭐⭐⭐⭐⭐ — A genuine point of confusion resolved with a clear, concrete distinction.

---

**Prompt 4 — Debugging the anomaly dimension mismatch**
> *"I'm getting `ValueError: dimensions ('month',) must have the same length as data` when subtracting a monthly climatology. What's wrong and how do I fix it?"*

<<<<<<< HEAD
**Response summary:** The AI identified the mismatch — a `(month,)` climatology cannot be subtracted from a `(time, lat, lon)` array directly. The fix is `da.groupby("time.month") - climatology`, which aligns dimensions automatically before subtracting.

**Helpfulness:** ⭐⭐⭐⭐⭐ — One-line fix that would have taken much longer to debug without help.

---

**Prompt 5 — Debugging the pcolormesh 3D array error**
> *"My `pcolormesh` plot is failing after `.sel(time='2021-04')`. The array shape is `(1, 20, 20)` but pcolormesh expects 2D. How do I fix this?"*

**Response summary:** The AI explained that `.sel()` on a single value can retain the time dimension at length 1. Chaining `.squeeze()` drops all length-1 dimensions, giving the expected `(20, 20)` shape for plotting.

**Helpfulness:** ⭐⭐⭐⭐⭐ — This was a real bug encountered during development. Fix: `anomaly.sel(time="2021-04").squeeze()`.

---

## 7. Common Issues & Fixes

### ❌ `ValueError: dictionary update sequence element #0 has length 4; 2 is required`
**Cause:** Calling `dict(da.dims)` — `da.dims` is a tuple of strings like `('time', 'lat', 'lon')`, not key-value pairs, so `dict()` fails on it.

**Fix:**
```python
print(da.dims)            # ('time', 'lat', 'lon')  ✅
print(dict(da.sizes))     # {'time': 36, 'lat': 20, 'lon': 20}  ✅
```
Reference: [xarray docs — DataArray properties](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.dims.html)

---

### ❌ `ValueError: dimensions ('month',) must have the same length as data`
**Cause:** Subtracting a climatology `DataArray` directly from a time series — the `month` and `time` dimensions don't align.

**Fix:**
```python
climatology = da.groupby("time.month").mean("time")
anomaly     = da.groupby("time.month") - climatology    # ✅ auto-aligns
```

---

### ❌ `pcolormesh` fails with shape `(1, 20, 20)` after `.sel()`
**Cause:** Selecting a single time step retains a length-1 time dimension; `pcolormesh` requires a 2D array.

**Fix:**
```python
april = anomaly.sel(time="2021-04").squeeze()    # drops length-1 dims ✅
```

---

### ❌ `KeyError` when using `.sel()`
**Cause:** The exact coordinate value doesn't exist in the grid.

**Fix:**
```python
da.sel(lat=1.23456, method="nearest")    # nearest-neighbour lookup ✅
```

---

### ❌ `ModuleNotFoundError: No module named 'xarray'`
**Cause:** Package not installed, or installed in a different Python environment than the one currently active.

**Fix:**
```bash
which python          # confirm the active environment (macOS/Linux)
pip install xarray
```

---

### ❌ Memory error with large `.nc` files
**Cause:** `xr.open_dataset()` loads everything into RAM at once.

**Fix:** Use Dask for lazy loading:
```bash
pip install dask
```
```python
ds = xr.open_dataset("large_file.nc", chunks={"time": 10})
```

---

## 8. References

### Official Documentation
- [xarray Docs](https://docs.xarray.dev/en/stable/) — Complete API reference
- [xarray User Guide](https://docs.xarray.dev/en/stable/user-guide/index.html) — Best starting point
- [xarray Examples Gallery](https://docs.xarray.dev/en/stable/examples/weather-data.html) — Weather data worked examples

### Real Satellite Data Sources
- [CHIRPS Rainfall](https://www.chc.ucsb.edu/data/chirps) — High-resolution rainfall for East Africa (1981–present)
- [MODIS NDVI MOD13A2](https://lpdaac.usgs.gov/products/mod13a2v061/) — 16-day NDVI composites at 1 km
- [NASA EarthData](https://earthdata.nasa.gov/) — Central portal for NASA satellite products
- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/) — ERA5 global climate reanalysis

### Tutorials & Courses
- [Project Pythia – xarray](https://foundations.projectpythia.org/core/xarray.html) — Beginner-to-intermediate curriculum
- [Earth and Environmental Data Science (Columbia)](https://earth-env-data-science.github.io/) — Open university course
- [Software Carpentry: Python for Atmosphere and Ocean Scientists](https://carpentries-lab.github.io/python-aos-lesson/) — Practical workshop
- [Pangeo Gallery](https://gallery.pangeo.io/) — Real-world xarray notebooks

### Helpful Blog Posts
- [Handling NetCDF files with xarray for beginners](https://towardsdatascience.com/handling-netcdf-files-using-xarray-for-absolute-beginners-111a8ab4463f) — Towards Data Science
- [NDVI analysis in Python](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/) — Earth Lab, University of Colorado

### Related Libraries to Explore Next
- [`rioxarray`](https://corteva.github.io/rioxarray/) — Raster I/O and CRS-aware operations
- [`cartopy`](https://scitools.org.uk/cartopy/) — Map projections for geospatial plotting
- [`dask`](https://dask.org/) — Parallel computing for large datasets

---

## 📁 Repository Structure

```
xarray-toolkit/
├── README.md                         ← This file
├── TOOLKIT.md                        ← Extended capstone reference document
├── requirements.txt                  ← Python dependencies
├── notebooks/
│   ├── 01_xarray_basics.ipynb        ← Core xarray concepts
│   ├── 02_rainfall_timeseries.ipynb  ← Rainfall climatology & anomalies
│   └── 03_ndvi_analysis.ipynb        ← NDVI satellite time series
├── scripts/
│   ├── rainfall_analysis.py          ← Standalone rainfall script
│   └── ndvi_analysis.py              ← Standalone NDVI script
└── data/
    └── README.md                     ← How synthetic data is generated
```

---

*MIT License — free to use and adapt for learning.*
=======
MIT License — free to use and adapt for learning.
>>>>>>> c6df480d5beb50cc7b5eefde1fc47f4a42e1b551
