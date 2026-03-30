# Data Directory

This project uses **synthetically generated data** — no downloads required.

All datasets are created programmatically inside the scripts and notebooks using `numpy` and `xarray`. This means:

- ✅ No large files to download
- ✅ Works offline
- ✅ Reproducible results

## What data is simulated?

### Rainfall Dataset (`rainfall_analysis.py`)
- **Dimensions**: `time × lat × lon`
- **Time**: 3 years of monthly data (2020–2022), 36 timesteps
- **Spatial grid**: 20×20 grid covering East Africa (-5°N to 15°N, 30°E to 50°E)
- **Values**: Simulated monthly rainfall (mm/day) with seasonal cycles and spatial gradients
- **Pattern**: Models a double-rainy-season regime typical of equatorial East Africa

### NDVI Dataset (`ndvi_analysis.py`)
- **Dimensions**: `time × lat × lon`
- **Time**: 3 years of 16-day composite data (similar to MODIS MOD13A2)
- **Spatial grid**: 20×20 grid
- **Values**: NDVI ranging from 0.1 (bare/arid) to 0.85 (dense vegetation)
- **Pattern**: Seasonal greening correlated to rainfall, with spatial variation (highlands vs lowlands)

## Real-world equivalents

In a real project, you would replace synthetic data with:

| Dataset | Source | Format |
|---------|--------|--------|
| CHIRPS rainfall | [climateserv.servirglobal.net](https://climateserv.servirglobal.net) | NetCDF (.nc) |
| MODIS NDVI | [NASA EarthData](https://earthdata.nasa.gov) | HDF / NetCDF |
| ERA5 climate reanalysis | [Copernicus CDS](https://cds.climate.copernicus.eu) | NetCDF (.nc) |
| TAMSAT rainfall | [University of Reading](https://www.tamsat.org.uk) | NetCDF (.nc) |

Loading a real `.nc` file with xarray is as simple as:
```python
import xarray as xr
ds = xr.open_dataset("chirps_rainfall.nc")
```