# Historical Weather Data Analysis

An interactive Streamlit dashboard and Jupyter notebook for exploring historical weather observations.

## Dataset
The project uses `weather_data.csv` (96,453 rows and 14 columns). The dataset includes temperature, apparent temperature, humidity, wind speed, visibility, pressure, precipitation type, summary and date fields.

**Data limitation:** There is no country/place column. The project uses a date-range filter and compares yearly averages instead of comparing countries. Multiple observations may share a calendar date, so only exact duplicate rows are removed.

## Key findings
Run `weather_analysis.ipynb` to calculate the exact findings from the dataset. The notebook reports:
1. The distribution and typical values of temperature.
2. The distribution and typical values of humidity and wind speed.
3. The relationship between temperature and humidity.
4. The difference between actual and apparent temperature.
5. Weather trends over the dataset's date range.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — interactive Streamlit dashboard
- `weather_data.csv` — source dataset
- `weather_analysis.ipynb` — full analysis notebook
- `requirements.txt` — Python dependencies
- `.gitignore` — excludes virtual environments and secrets

## Live app
https://weather-data-analysis-2222.streamlit.app/
