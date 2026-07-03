# Myntra Review Scrapper System

This repository contains a Streamlit-based Myntra review scraping and analysis project, plus a few legacy files from an earlier Flask version. The main purpose of this README is to explain the project structure so it is easier to navigate, maintain, and extend.

## Project Structure

```text
MyntraReviewScrapperSystem/
├── app.py
├── application.py
├── main.py
├── data.csv 
├── myntra.ipynb
├── packages.txt
├── README.md
├── requirements.txt
├── runtime.txt
├── setup.py
├── database_connect/
├── pages/
│   └── generate_analysis.py
├── scripts/
│   └── scheduled_scrape.py
├── src/
│   ├── __init__.py
│   ├── exception.py
│   ├── cloud_io/
│   │   └── __init__.py
│   ├── constants/
│   │   └── __init__.py
│   ├── data_report/
│   │   ├── __init__.py
│   │   └── generate_data_report.py
│   ├── scrapper/
│   │   ├── __init__.py
│   │   ├── scrape.py
│   │   └── providers/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       └── myntra.py
│   ├── ui/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── static/
│   └── css/
│       ├── main.css
│       ├── streamlit.css
│       └── style.css
└── templates/
    ├── base.html
    ├── index.html
    └── results.html
```

## Root Files

`app.py` is the main Streamlit application. It builds the user interface, accepts product input, triggers scraping, loads saved reviews from MongoDB, and renders the results.

`main.py` is the Streamlit entry point. It simply imports `app.py`, which makes `streamlit run main.py` and `streamlit run app.py` behave the same way.

`application.py` is a legacy Flask entry point. It serves the HTML templates in `templates/` and uses the scraper for the older web app flow.

`requirements.txt`, `packages.txt`, `runtime.txt`, and `setup.py` describe the environment and deployment dependencies.

`data.csv` is sample or saved data for analysis.

`myntra.ipynb` is the notebook version of the work, useful for experimentation and debugging.

`database_connect/` is currently empty in this workspace.

## `src/` Package

The `src/` folder contains the reusable Python logic used by the app.

`src/exception.py` defines the custom exception wrapper used across the project.

`src/constants/` stores shared constants such as session keys and database names.

`src/cloud_io/` contains MongoDB access logic. The `MongoIO` class handles connecting to MongoDB, saving scraped reviews, and reading saved reviews back.

`src/scrapper/` contains the scraping workflow.

`src/scrapper/scrape.py` is the main Selenium and BeautifulSoup scraper that searches Myntra, opens product pages, and extracts review data.

`src/scrapper/providers/` is set up for provider-specific scraping logic. `base.py` can be used as a shared interface, while `myntra.py` is the Myntra-specific provider.

`src/data_report/` contains analysis/reporting code. `generate_data_report.py` builds dashboards and summary views from scraped review data.

`src/utils/` contains helper functions used by the UI and data-loading flow.

`src/ui/` is reserved for reusable UI helpers or components.

## UI and Presentation Files

`pages/generate_analysis.py` is the Streamlit multipage analysis screen. It reads review data, builds charts, and shows detailed review tables.

`static/css/` stores custom CSS for both the Streamlit and Flask interfaces.

`templates/` contains the HTML templates used by the Flask version of the app.

## Scripts

`scripts/scheduled_scrape.py` is intended for automated or scheduled scraping runs.

## How The Pieces Fit Together

1. The user opens the Streamlit app through `app.py` or `main.py`.
2. The scraper in `src/scrapper/scrape.py` collects Myntra review data.
3. MongoDB access is handled by `src/cloud_io/`.
4. The analysis page in `pages/generate_analysis.py` presents charts, tables, and summary metrics.
5. Styling comes from the files in `static/css/`.

## Notes

- The Streamlit version is the primary interface for this workspace.
- The Flask files and templates are still present, but they are legacy support files.
- The project is organized so scraping, storage, analysis, and UI code stay separated.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

If you want, I can also turn this into a more polished README with badges, setup steps, and a cleaner architecture diagram.