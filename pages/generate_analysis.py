import pandas as pd
import streamlit as st
import plotly.express as px
import warnings
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY
from src.utils import fetch_product_names_from_cloud
from src.data_report.generate_data_report import DashboardGenerator

# Suppress FutureWarning from plotly/pandas groupby operations
warnings.filterwarnings('ignore', category=FutureWarning, module='plotly')

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
    }
    
    h1 {
        color: #FF6B6B !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #4ECDC4 !important;
        border-bottom: 3px solid #FFE66D !important;
        padding-bottom: 0.5rem !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: #333333 !important;
        font-size: 1.2rem !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255,107,107,0.4) !important;
    }
    
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 1.5rem !important;
        border-radius: 10px !important;
        color: white !important;
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
    
    [data-testid="stSidebar"] .stAlert {
        background-color: rgba(78, 205, 196, 0.2) !important;
        border: 2px solid #4ECDC4 !important;
    }
    
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: #2D3A4A !important;
        color: white !important;
        border: 2px solid #4ECDC4 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("📊 Review Analysis Dashboard")
    st.markdown("#### Detailed Insights & Analytics", unsafe_allow_html=True)

st.markdown("---")


def create_analysis_page(review_data: pd.DataFrame):
    """Create a comprehensive analysis page"""
    if review_data is not None and not review_data.empty:
        
        # Display data statistics
        st.subheader("📈 Quick Statistics")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("📝 Total Reviews", len(review_data))
        
        with stat_col2:
            try:
                avg_rating = pd.to_numeric(review_data['Rating'].str.replace('★', '').str.split().str[0], errors='coerce').mean()
                st.metric("⭐ Average Rating", f"{avg_rating:.1f}" if not pd.isna(avg_rating) else "N/A")
            except:
                st.metric("⭐ Average Rating", "N/A")
        
        with stat_col3:
            st.metric("🛍️ Products", len(review_data['Product Name'].unique()))
        
        with stat_col4:
            st.metric("👥 Unique Users", len(review_data['Name'].unique()))
        
        st.markdown("---")
        
        # Tabbed interface for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Full Data", "🔍 Detailed View", "📊 Analytics", "🎯 Analysis"])
        
        with tab1:
            st.subheader("Data Overview")
            st.dataframe(review_data, use_container_width=True, height=500)
            
            # Download button
            csv = review_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name="reviews_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with tab2:
            st.subheader("Individual Review Details")
            # Create a searchable view
            col1, col2 = st.columns([2, 1])
            with col1:
                search_term = st.text_input("🔍 Search in reviews", placeholder="Search by product, rating, or user name")
            
            if search_term:
                filtered_data = review_data[
                    review_data.astype(str).agg(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                ]
                st.write(f"**Found {len(filtered_data)} matching reviews**")
                for idx, row in filtered_data.iterrows():
                    with st.expander(f"🔸 {row['Product Name']} - {row['Name']} - {row['Rating']}"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"**Product:** {row['Product Name']}")
                            st.write(f"**User:** {row['Name']}")
                            st.write(f"**Comment:** {row['Comment']}")
                        with col2:
                            st.write(f"**Rating:** {row['Rating']}")
                            st.write(f"**Price:** {row['Price']}")
                            st.write(f"**Date:** {row['Date']}")
            else:
                for idx, row in review_data.iterrows():
                    with st.expander(f"🔸 {row['Product Name']} - {row['Name']} - {row['Rating']}"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"**Product:** {row['Product Name']}")
                            st.write(f"**User:** {row['Name']}")
                            st.write(f"**Comment:** {row['Comment']}")
                        with col2:
                            st.write(f"**Rating:** {row['Rating']}")
                            st.write(f"**Price:** {row['Price']}")
                            st.write(f"**Date:** {row['Date']}")
        
        with tab3:
            st.subheader("Review Analytics")
            
            # Rating distribution
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**Rating Distribution**")
                try:
                    # Get rating counts
                    rating_counts = review_data['Rating'].astype(str).value_counts()
                    
                    if len(rating_counts) > 0:
                        # Create DataFrame for plotly
                        rating_df = pd.DataFrame({
                            'Rating': rating_counts.index,
                            'Count': rating_counts.values
                        })
                        
                        # Create bar chart with plotly
                        fig = px.bar(rating_df, x='Rating', y='Count', 
                                    title='Ratings Distribution',
                                    color='Count',
                                    color_continuous_scale='Viridis',
                                    height=400)
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No rating data available")
                except Exception as e:
                    st.warning("Chart unavailable")
                    # Fallback: display as list
                    rating_counts = review_data['Rating'].astype(str).value_counts()
                    for rating, count in rating_counts.items():
                        st.write(f"• {rating}: {count} reviews")
            
            with col2:
                st.write("**Product Distribution**")
                try:
                    # Get top 10 products
                    product_counts = review_data['Product Name'].value_counts().head(10)
                    
                    if len(product_counts) > 0:
                        product_df = pd.DataFrame({
                            'Product': product_counts.index,
                            'Reviews': product_counts.values
                        })
                        
                        fig = px.bar(product_df, y='Product', x='Reviews', 
                                    title='Top 10 Products',
                                    orientation='h',
                                    color='Reviews',
                                    color_continuous_scale='Blues',
                                    height=400)
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No product data available")
                except Exception as e:
                    st.warning("Chart unavailable")
                    # Fallback: display as list
                    for idx, (product, count) in enumerate(review_data['Product Name'].value_counts().head(10).items(), 1):
                        st.write(f"• {product} - {count} reviews")
            
            st.markdown("---")
            
            # More analytics
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**User Reviews Count (Top Users)**")
                try:
                    # Get top 10 users
                    user_counts = review_data['Name'].value_counts().head(10)
                    
                    if len(user_counts) > 0:
                        user_df = pd.DataFrame({
                            'User': user_counts.index,
                            'Reviews': user_counts.values
                        })
                        
                        fig = px.bar(user_df, y='User', x='Reviews',
                                    title='Top 10 Users',
                                    orientation='h',
                                    color='Reviews',
                                    color_continuous_scale='Reds',
                                    height=400)
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No user data available")
                except Exception as e:
                    st.warning("Chart unavailable")
                    # Fallback: display as list
                    for idx, (user, count) in enumerate(review_data['Name'].value_counts().head(10).items(), 1):
                        st.write(f"{idx}. {user} - {count} review(s)")
            
            with col2:
                st.write("**Review Comment Length Statistics**")
                try:
                    # Handle comments
                    comments = review_data['Comment'].astype(str)
                    comments = comments[comments != 'No comment Given']
                    
                    if len(comments) > 0:
                        comment_lengths = comments.str.len()
                        
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        with col_stat1:
                            st.metric("📏 Avg", f"{comment_lengths.mean():.0f} chars")
                        with col_stat2:
                            st.metric("📈 Max", f"{comment_lengths.max()} chars")
                        with col_stat3:
                            st.metric("📉 Min", f"{comment_lengths.min()} chars")
                        
                        # Show length distribution with buckets
                        st.write("*Length Distribution:*")
                        length_buckets = pd.cut(comment_lengths, bins=5)
                        length_dist = length_buckets.value_counts().sort_index()
                        
                        # Create histogram with plotly
                        hist_data = []
                        for interval, count in length_dist.items():
                            hist_data.append({'Range': str(interval), 'Count': count})
                        
                        hist_df = pd.DataFrame(hist_data)
                        fig = px.bar(hist_df, x='Range', y='Count',
                                    title='Comment Length Distribution',
                                    color='Count',
                                    color_continuous_scale='Greens',
                                    height=350)
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No comment data available")
                except Exception as e:
                    st.warning("Chart unavailable")
                    # Fallback: just show stats
                    comments = review_data['Comment'].astype(str)
                    comments = comments[comments != 'No comment Given']
                    if len(comments) > 0:
                        comment_lengths = comments.str.len()
                        st.write(f"📏 **Average:** {comment_lengths.mean():.0f} chars")
                        st.write(f"📈 **Maximum:** {comment_lengths.max()} chars")
                        st.write(f"📉 **Minimum:** {comment_lengths.min()} chars")
        
        with tab4:
            st.subheader("Detailed Analysis Report")
            if st.button("🚀 Generate Full Analysis"):
                with st.spinner("📊 Generating comprehensive analysis..."):
                    try:
                        dashboard = DashboardGenerator(review_data)
                        
                        # Display general information
                        st.write("**General Information:**")
                        dashboard.display_general_info()
                        
                        st.markdown("---")
                        
                        # Display product-specific sections
                        st.write("**Product Sections:**")
                        dashboard.display_product_sections()
                        
                        st.success("✅ Analysis completed successfully!")
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)[:200]}")
    
    else:
        st.warning("⚠️ No data available for analysis")


# Main logic
try:
    if st.session_state.get("data", False):
        st.subheader("📍 Getting Review Data...")
        
        data = None
        
        # Try to get data from MongoDB, fallback to session state
        try:
            mongo_con = MongoIO()
            product_name = st.session_state.get(SESSION_PRODUCT_KEY, "")
            if product_name:
                data = mongo_con.get_reviews(product_name=product_name)
            else:
                data = st.session_state.get("latest_scrapped_data")
        except Exception as e:
            # Fallback to session data if MongoDB is unavailable
            data = st.session_state.get("latest_scrapped_data")
            error_msg = str(e)
            if "DNS" in error_msg or "resolution" in error_msg or "timed out" in error_msg:
                st.info("ℹ️ Using current session data (MongoDB unavailable due to DNS/network timeout)")
            else:
                st.info("ℹ️ Using current session data (MongoDB unavailable)")
        
        create_analysis_page(data)
    
    else:
        st.markdown("""
            <div style='text-align: center; padding: 3rem;'>
                <h3>📭 No Data Available</h3>
                <p>Please go to the <strong>Search</strong> page to scrape reviews first.</p>
            </div>
        """, unsafe_allow_html=True)

except AttributeError:
    st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <h3>📭 No Data Available</h3>
            <p>Please go to the <strong>Search</strong> page to scrape reviews first.</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About Analysis")
    st.info(
        """
        **Analysis Dashboard Features:**
        - 📈 Quick statistics overview
        - 🔍 Detailed review search
        - 📊 Analytics and charts
        - 🎯 Comprehensive analysis
        - 📥 Export data as CSV
        """
    )
    
    if "latest_scrapped_data" in st.session_state:
        data = st.session_state["latest_scrapped_data"]
        st.markdown("---")
        st.markdown("### 📊 Data Info")
        st.write(f"**Reviews:** {len(data)}")
        st.write(f"**Columns:** {len(data.columns)}")
        st.write(f"**Last Updated:** Just now")


