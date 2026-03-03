import pandas as pd
import streamlit as st
import os
from pathlib import Path
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY
from src.utils import fetch_product_names_from_cloud


st.set_page_config(
    page_title="Myntra Review Scraper",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _inject_css(path: str) -> None:
    try:
        css = Path(path).read_text(encoding="utf-8")
    except Exception:
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


_inject_css("static/css/streamlit.css")

# Header section with info
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🛍️ Myntra Review Scraper")
    st.markdown("#### Extract and Analyze Customer Reviews Instantly", unsafe_allow_html=True)

st.markdown("---")

if "data" not in st.session_state:
    st.session_state["data"] = False


def _get_setting(key: str) -> str | None:
    value = os.getenv(key)
    if value:
        return value
    try:
        return st.secrets.get(key)  # type: ignore[attr-defined]
    except Exception:
        return None


def _cloud_read_only_mode() -> bool:
    # Streamlit Community Cloud runs on Linux; Myntra is commonly blocked there.
    # Default to MongoDB-read mode on non-Windows.
    forced = (_get_setting("FORCE_MONGODB_READ") or "").strip().lower() in {"1", "true", "yes"}
    return forced or os.name != "nt"


def _render_reviews_table(df: pd.DataFrame, product_name: str, title: str) -> None:
    st.markdown("---")
    st.subheader(f"📈 {title} ({len(df)} reviews)")
    st.dataframe(df, use_container_width=True, height=400)

    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{product_name.replace(' ', '_')}_reviews.csv",
        mime="text/csv",
        use_container_width=True,
    )


def _load_saved_reviews_from_mongodb(product_name: str) -> pd.DataFrame | None:
    mongo_url = _get_setting("MONGODB_URL")
    if not mongo_url:
        st.info(
            "To use the deployed app, set `MONGODB_URL` in Streamlit Cloud Secrets "
            "(App settings → Secrets). Then the app can load previously saved reviews."
        )
        return None

    mongoio = MongoIO()
    existing = mongoio.get_reviews(product_name=product_name)
    if not existing:
        available: list[str]
        try:
            if mongoio.mongo_db is not None:
                available = mongoio.mongo_db.list_collection_names()
            else:
                available = []
        except Exception:
            available = []

        requested_collection = product_name.replace(" ", "_")
        if not available:
            st.warning(
                "No saved reviews were found in MongoDB for this product name. "
                "Also, no collections were found in the configured database, so either nothing has been saved yet "
                "or this MongoDB user/URI does not have access to the expected database."
            )
            st.info(
                "Checks: (1) In your local run, confirm you saw 'Data scraped and saved to MongoDB successfully!'. "
                "(2) In MongoDB Atlas → Data Explorer, look for database 'myntra-reviews' and collections like 'blue_shirt'. "
                "(3) Ensure the same `MONGODB_URL` (and optional `MONGODB_FALLBACK_URL`) is set in Streamlit Secrets."
            )
            return None

        if requested_collection not in set(available):
            shown = [name.replace("_", " ") for name in available[:25]]
            st.warning(
                "No saved reviews were found because this product name does not match any saved MongoDB collection. "
                "Select a saved product from the dropdown (if available) or use one of the saved names shown below."
            )
            st.info(
                f"Saved products found: {len(available)}\n\n" + "\n".join(f"- {p}" for p in shown)
            )
            return None

        st.warning(
            "No saved reviews were found in MongoDB for this product name. "
            "Tip: run the scraper locally once to populate MongoDB, then refresh this app."
        )
        return None

    df = pd.DataFrame(existing)
    if df.empty:
        st.warning("Saved MongoDB data exists but is empty for this product.")
        return None
    return df


def form_input():
    cloud_read_only_mode = _cloud_read_only_mode()

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
            ,
            disabled=cloud_read_only_mode,
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
            try:
                fallback_df = _load_saved_reviews_from_mongodb(product)
                if fallback_df is None:
                    return

                st.session_state["data"] = True
                st.session_state["latest_scrapped_data"] = fallback_df
                st.session_state[SESSION_PRODUCT_KEY] = product
                _render_reviews_table(fallback_df, product, title="Saved Data")
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
                                if not available:
                                    st.warning(
                                        "Live scraping is blocked, and no collections were found in the configured MongoDB database. "
                                        "This usually means MongoDB is pointing to a different cluster/user/db than the one you saved data into, "
                                        "or nothing has been saved yet."
                                    )
                                    st.info(
                                        "In Atlas Data Explorer, confirm database 'myntra-reviews' exists and contains collections for your products."
                                    )
                                elif requested_collection not in set(available):
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
