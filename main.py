import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Myntra Review Scraper",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': "https://github.com",
        'About': "# Myntra Review Scraper\nA powerful tool to extract and analyze customer reviews from Myntra"
    }
)

# Define pages
scraper_page = st.Page("app.py", title="🛍️ Scraper", icon="🛍️", default=True)
analysis_page = st.Page("pages/generate_analysis.py", title="📊 Analysis", icon="📊")

# Create navigation
pg = st.navigation([scraper_page, analysis_page])

# Run the selected page
pg.run()
