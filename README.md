# 🛰️ xarray Beginner's Toolkit
### Satellite Time Series Analysis: Rainfall Patterns & NDVI

> A beginner-friendly guide to working with large gridded datasets using `xarray` in Python.  
> Built as a Moringa AI Capstone Project — *"Prompt-Powered Kickstart"*

---

## 📦 What's in this Repo?

```
xarray-toolkit/
├── README.md                    ← You are here
├── TOOLKIT.md                   ← Full beginner's guide (the capstone document)
├── requirements.txt             ← Python dependencies
├── notebooks/
│   ├── 01_xarray_basics.ipynb   ← Core xarray concepts
│   ├── 02_rainfall_timeseries.ipynb  ← Rainfall pattern analysis
│   └── 03_ndvi_analysis.ipynb   ← NDVI satellite time series
├── scripts/
│   ├── rainfall_analysis.py     ← Standalone rainfall script
│   └── ndvi_analysis.py         ← Standalone NDVI script
└── data/
    └── README.md                ← How synthetic data is generated
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/xarray-toolkit.git
cd xarray-toolkit
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the scripts
```bash
# Rainfall pattern analysis
python scripts/rainfall_analysis.py

# NDVI satellite time series
python scripts/ndvi_analysis.py
```

### 5. Or launch Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

---

## 🎯 What You'll Learn

- What `xarray` is and why it's used for climate & satellite data
- How to create and manipulate multi-dimensional `DataArray` and `Dataset` objects
- How to work with time series data along spatial grids
- How to compute temporal statistics (monthly means, seasonal anomalies)
- How to visualize rainfall and NDVI patterns using `matplotlib`

---

## 🧠 AI-Assisted Learning

This entire toolkit was scaffolded using **Claude (Anthropic)**. The `TOOLKIT.md` document includes a full **AI Prompt Journal** showing which prompts were used, what the AI returned, and how it accelerated learning. See [TOOLKIT.md](https://github.com/EstherWMaina/Xarray-Beginner-Toolkit/blob/main/Toolkit.md).

---

## 📋 Requirements

| Tool | Version |
|------|---------|
| Python | 3.8+ |
| xarray | 2023.x+ |
| numpy | 1.24+ |
| matplotlib | 3.7+ |
| pandas | 2.0+ |
| jupyter | 1.0+ |

---

## 📖 Full Guide

See **[TOOLKIT.md](TOOLKIT.md)** for the complete beginner's toolkit document including setup, examples, common errors, and references.

---

## 📄 License

MIT License — free to use and adapt for learning.
