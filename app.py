import pandas as pd
import streamlit as st
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    /* Main app styling */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --accent-color: #FFE66D;
        --dark-bg: #1A1A2E;
        --light-bg: #F7F7F7;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
    }
    
    /* Title styling */
    h1 {
        color: #FF6B6B !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    h2 {
        color: #4ECDC4 !important;
        border-bottom: 3px solid #FFE66D !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #4ECDC4 !important;
        padding: 0.7rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255,107,107,0.4) !important;
    }
    
    /* Container styling */
    .stContainer {
        background: white !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07) !important;
    }
    
    /* Success/Warning/Info messages */
    .stAlert {
        border-radius: 8px !important;
    }
    
    [data-testid="stAlert"] {
        padding: 1rem !important;
        border-left: 4px solid !important;
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%) !important;
    }
    
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown {
        color: #E8E8E8 !important;
    }
    
    /* Sidebar checkboxes and inputs */
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: #2D3A4A !important;
        color: white !important;
        border: 2px solid #4ECDC4 !important;
    }
    
    /* Stats cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 1.5rem !important;
        border-radius: 10px !important;
        color: white !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Header section with info
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🛍️ Myntra Review Scraper")
    st.markdown("#### Extract and Analyze Customer Reviews Instantly", unsafe_allow_html=True)

st.markdown("---")

st.session_state["data"] = False


def form_input():
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Search Configuration")
        product = st.text_input(
            "🔍 Product Name",
            placeholder="Enter product name (e.g., 'blue shirt', 'running shoes')",
            help="Type the product name you want to scrape reviews for"
        )
    
    with col2:
        st.subheader("📊 Settings")
        no_of_products = st.number_input(
            "Number of Products",
            value=1,
            min_value=1,
            max_value=20,
            step=1,
            help="How many products to scrape (1-20)"
        )
    
    st.markdown("---")
    
    # Create columns for buttons and status
    btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])
    
    with btn_col1:
        scrape_button = st.button("🚀 Start Scraping", use_container_width=True, key="scrape_btn")
    
    if scrape_button:
        if not product.strip():
            st.error("❌ Please enter a product name to search!")
            return
        
        # Progress section
        with st.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info("⏳ Initializing scraper...")
            progress_bar.progress(15)
            
            try:
                # Lazy import so the app can deploy even if Selenium
                # dependencies fail to install on the platform.
                try:
                    from src.scrapper.scrape import ScrapeReviews
                except ModuleNotFoundError as e:
                    if e.name == "selenium":
                        st.error(
                            "Selenium is not installed in this environment. "
                            "On Streamlit Cloud, ensure `requirements.txt` is committed at the repo root and rebuild the app (Clear cache + Reboot)."
                        )
                        return
                    raise

                scrapper = ScrapeReviews(
                    product_name=product,
                    no_of_products=int(no_of_products)
                )
                
                status_text.info("🔄 Scraping reviews from Myntra...")
                progress_bar.progress(50)
                
                scrapped_data = scrapper.get_review_data()
                progress_bar.progress(85)
                
                if scrapped_data is not None and not scrapped_data.empty:
                    st.session_state["data"] = True
                    st.session_state["latest_scrapped_data"] = scrapped_data
                    
                    # Try to store in MongoDB, but don't crash if it fails
                    try:
                        mongoio = MongoIO()
                        mongoio.store_reviews(product_name=product,
                                              reviews=scrapped_data)
                        progress_bar.progress(100)
                        st.success("✅ Data scraped and saved to MongoDB successfully!")
                        status_text.empty()
                    except Exception as e:
                        progress_bar.progress(100)
                        error_msg = str(e)
                        if "DNS" in error_msg or "resolution" in error_msg or "timed out" in error_msg:
                            st.warning("⚠️ MongoDB is unreachable (DNS/network timeout).\n\nYour scraped data is shown below and available for analysis in this session, but not saved to the database.")
                        else:
                            st.warning(f"⚠️ Could not save to MongoDB: {error_msg[:100]}...\n\nData is shown below and available in this session.")
                        print(f"MongoDB error: {error_msg}")
                        status_text.empty()
                    
                    # Display results
                    st.markdown("---")
                    st.subheader(f"📈 Scraped Data ({len(scrapped_data)} reviews)")
                    
                    # Display data stats
                    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                    with stat_col1:
                        st.metric("Total Reviews", len(scrapped_data))
                    with stat_col2:
                        avg_rating = pd.to_numeric(scrapped_data['Rating'].str.replace('★', '').str.split().str[0], errors='coerce').mean()
                        st.metric("Avg Rating", f"{avg_rating:.1f}★" if not pd.isna(avg_rating) else "N/A")
                    with stat_col3:
                        st.metric("Products", len(scrapped_data['Product Name'].unique()))
                    with stat_col4:
                        st.metric("Unique Users", len(scrapped_data['Name'].unique()))
                    
                    st.markdown("---")
                    st.markdown("#### Data Preview")
                    st.dataframe(scrapped_data, use_container_width=True, height=400)
                    
                    # Download button
                    csv = scrapped_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name=f"{product.replace(' ', '_')}_reviews.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                else:
                    progress_bar.progress(100)
                    st.warning("⚠️ No reviews found for the specified product. Try a different product name.")
                    status_text.empty()
                    
            except Exception as e:
                progress_bar.progress(0)
                st.error(f"❌ Error during scraping: {str(e)[:500]}")
                status_text.empty()


# Sidebar info
with st.sidebar:
    st.markdown("### 📚 About")
    st.info(
        """
        **Myntra Review Scraper** helps you:
        - 🔍 Extract customer reviews from Myntra
        - 📊 Analyze product sentiment
        - 💾 Store data for further analysis
        - 📈 Generate insights from reviews
        """
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    if st.checkbox("Show data statistics"):
        if "latest_scrapped_data" in st.session_state:
            data = st.session_state["latest_scrapped_data"]
            st.write(f"**Rows:** {len(data)}")
            st.write(f"**Columns:** {len(data.columns)}")


# Run the main function
form_input()
