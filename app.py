import pandas as pd
import streamlit as st
import os
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY
from src.utils import fetch_product_names_from_cloud

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

if "data" not in st.session_state:
    st.session_state["data"] = False


def form_input():
    # Streamlit Community Cloud runs on Linux; Myntra is commonly blocked there.
    # In that environment we default to reading previously saved data from MongoDB.
    cloud_read_only_mode = os.name != "nt" or os.getenv("FORCE_MONGODB_READ", "").strip() in {"1", "true", "True"}

    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Search Configuration")

        product = ""
        if cloud_read_only_mode:
            saved_products: list[str] = []
            try:
                saved_products = fetch_product_names_from_cloud()
            except Exception:
                saved_products = []

            if saved_products:
                selected_product = st.selectbox(
                    "📂 Saved Product (MongoDB)",
                    options=saved_products,
                    help="On Streamlit Cloud, the app loads previously saved reviews from MongoDB",
                )
                product = selected_product
            else:
                product = st.text_input(
                    "🔍 Product Name",
                    placeholder="Enter saved product name (must match MongoDB collection)",
                    help="On Streamlit Cloud, live scraping is restricted; enter a product name already saved in MongoDB",
                )
        else:
            product = st.text_input(
                "🔍 Product Name",
                placeholder="Enter product name (e.g., 'blue shirt', 'running shoes')",
                help="Type the product name you want to scrape reviews for",
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
        button_label = "📥 Load Saved Reviews" if cloud_read_only_mode else "🚀 Start Scraping"
        scrape_button = st.button(button_label, use_container_width=True, key="scrape_btn")
    
    if scrape_button:
        if not product.strip():
            st.error("❌ Please enter a product name to search!")
            return

        # In cloud/read-only mode, skip Selenium scraping entirely.
        if cloud_read_only_mode:
            mongo_url = os.getenv("MONGODB_URL")
            if not mongo_url:
                try:
                    mongo_url = st.secrets.get("MONGODB_URL")
                except Exception:
                    mongo_url = None
            if not mongo_url:
                st.info(
                    "To use the deployed app, set `MONGODB_URL` in Streamlit Cloud Secrets "
                    "(App settings → Secrets). Then the app can load previously saved reviews."
                )
                return

            try:
                mongoio = MongoIO()
                existing = mongoio.get_reviews(product_name=product)
                if not existing:
                    try:
                        if mongoio.mongo_db is not None:
                            available = mongoio.mongo_db.list_collection_names()
                        else:
                            available = []
                    except Exception:
                        available = []

                    requested_collection = product.replace(" ", "_")
                    if available and requested_collection not in set(available):
                        shown = [name.replace("_", " ") for name in available[:25]]
                        st.warning(
                            "No saved reviews were found because this product name does not match any saved MongoDB collection. "
                            "Select a saved product from the dropdown (if available) or use one of the saved names shown below."
                        )
                        st.info(
                            f"Saved products found: {len(available)}\n\n" + "\n".join(f"- {p}" for p in shown)
                        )
                    else:
                        st.warning(
                            "No saved reviews were found in MongoDB for this product name. "
                            "Tip: run the scraper locally once to populate MongoDB, then refresh this app."
                        )
                    return

                fallback_df = pd.DataFrame(existing)
                if fallback_df.empty:
                    st.warning("Saved MongoDB data exists but is empty for this product.")
                    return

                st.session_state["data"] = True
                st.session_state["latest_scrapped_data"] = fallback_df
                st.session_state[SESSION_PRODUCT_KEY] = product

                st.markdown("---")
                st.subheader(f"📈 Saved Data ({len(fallback_df)} reviews)")
                st.dataframe(fallback_df, use_container_width=True, height=400)

                csv = fallback_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"{product.replace(' ', '_')}_reviews.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                return
            except Exception as mongo_e:
                st.error(f"❌ Could not load from MongoDB: {str(mongo_e)[:300]}")
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
                    st.session_state[SESSION_PRODUCT_KEY] = product
                    
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
                error_text = str(e)
                st.error(f"❌ Error during scraping: {error_text[:500]}")

                # If Myntra blocks scraping on Streamlit Cloud, try a graceful fallback:
                # show previously saved data from MongoDB (if available).
                blocked_signals = (
                    "captcha" in error_text.lower()
                    or "access denied" in error_text.lower()
                    or "site maintenance" in error_text.lower()
                    or "blocked" in error_text.lower()
                )
                if blocked_signals:
                    mongo_url = os.getenv("MONGODB_URL")
                    if not mongo_url:
                        try:
                            mongo_url = st.secrets.get("MONGODB_URL")
                        except Exception:
                            mongo_url = None
                    if not mongo_url:
                        st.info(
                            "Live scraping is blocked on Streamlit Cloud for Myntra. "
                            "To show saved reviews here, set `MONGODB_URL` in Streamlit Cloud Secrets (App settings → Secrets)."
                        )
                    else:
                        try:
                            mongoio = MongoIO()
                            existing = mongoio.get_reviews(product_name=product)

                            if not existing:
                                try:
                                    if mongoio.mongo_db is not None:
                                        available = mongoio.mongo_db.list_collection_names()
                                    else:
                                        available = []
                                except Exception:
                                    available = []

                                requested_collection = product.replace(" ", "_")
                                if available and requested_collection not in set(available):
                                    shown = [name.replace("_", " ") for name in available[:25]]
                                    st.warning(
                                        "Live scraping is blocked, and this product name does not match any saved MongoDB collection. "
                                        "Use a saved product name shown below (or populate MongoDB locally)."
                                    )
                                    st.info(
                                        f"Saved products found: {len(available)}\n\n" + "\n".join(f"- {p}" for p in shown)
                                    )
                                else:
                                    st.warning(
                                        "Live scraping is blocked, and no saved reviews were found in MongoDB for this product name. "
                                        "Tip: run the scraper locally once (where Myntra allows it) to populate MongoDB, then the Cloud app can display that saved data."
                                    )
                            else:
                                fallback_df = pd.DataFrame(existing)
                                if fallback_df.empty:
                                    st.warning(
                                        "Live scraping is blocked, and the saved MongoDB data for this product is empty."
                                    )
                                else:
                                    st.warning(
                                        "Live scraping is blocked from this server. "
                                        "Showing previously saved reviews from MongoDB instead."
                                    )
                                    st.session_state["data"] = True
                                    st.session_state["latest_scrapped_data"] = fallback_df
                                    st.session_state[SESSION_PRODUCT_KEY] = product

                                    st.markdown("---")
                                    st.subheader(f"📈 Saved Data ({len(fallback_df)} reviews)")
                                    st.dataframe(fallback_df, use_container_width=True, height=400)

                                    csv = fallback_df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download as CSV",
                                        data=csv,
                                        file_name=f"{product.replace(' ', '_')}_reviews.csv",
                                        mime="text/csv",
                                        use_container_width=True,
                                    )
                                    progress_bar.progress(100)
                        except Exception as mongo_e:
                            st.warning(f"MongoDB fallback failed: {str(mongo_e)[:200]}")
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
