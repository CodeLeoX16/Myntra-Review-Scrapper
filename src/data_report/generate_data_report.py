import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os, sys
from src.exception import CustomException


class DashboardGenerator:
    def __init__(self, data):
        self.data = data

    def display_general_info(self):
        st.header('General Information')

        # Convert 'Over_All_Rating' and 'Price' columns to numeric
        self.data['Over_All_Rating'] = pd.to_numeric(self.data['Over_All_Rating'], errors='coerce')
        
        # Handle Price column - convert to string first, then remove currency symbol
        self.data['Price'] = pd.to_numeric(
            self.data['Price'].astype(str).str.replace("₹", "").str.replace(",", "").str.strip(),
            errors='coerce')

        self.data["Rating"] = pd.to_numeric(self.data['Rating'].astype(str).str.replace('★', '').str.split().str[0], errors='coerce')

        # Summary pie chart of average ratings by product
        product_ratings = self.data.groupby('Product Name', as_index=False)['Over_All_Rating'].mean().dropna()

        fig_pie = px.pie(product_ratings, values='Over_All_Rating', names='Product Name',
                         title='Average Ratings by Product')
        st.plotly_chart(fig_pie)

        # Bar chart comparing average prices of different products with different colors
        avg_prices = self.data.groupby('Product Name', as_index=False)['Price'].mean().dropna()
        fig_bar = px.bar(avg_prices, x='Product Name', y='Price', color='Product Name',
                         title='Average Price Comparison Between Products',
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig_bar.update_xaxes(title='Product Name')
        fig_bar.update_yaxes(title='Average Price')
        st.plotly_chart(fig_bar)

    def display_product_sections(self):
        st.header('Product Sections')

        product_names = self.data['Product Name'].unique()
        
        if len(product_names) == 0:
            st.warning("No products found in data")
            return
        
        # Create columns based on number of products, max 3 columns
        num_columns = min(len(product_names), 3)
        columns = st.columns(num_columns)

        for i, product_name in enumerate(product_names):
            product_data = self.data[self.data['Product Name'] == product_name]
            col_index = i % num_columns

            with columns[col_index]:
                st.subheader(f'{product_name[:50]}...' if len(str(product_name)) > 50 else f'{product_name}')

                try:
                    # Display price in text or markdown with emojis
                    avg_price = product_data['Price'].mean()
                    if pd.notna(avg_price):
                        st.markdown(f"💰 Average Price: ₹{avg_price:.2f}")
                    else:
                        st.markdown(f"💰 Average Price: N/A")
                except:
                    st.markdown(f"💰 Average Price: N/A")

                try:
                    # Display average rating
                    avg_rating = product_data['Over_All_Rating'].mean()
                    if pd.notna(avg_rating):
                        st.markdown(f"⭐ Average Rating: {avg_rating:.2f}")
                    else:
                        st.markdown(f"⭐ Average Rating: N/A")
                except:
                    st.markdown(f"⭐ Average Rating: N/A")

                try:
                    # Display top positive comments with great ratings
                    positive_reviews = product_data[pd.to_numeric(product_data['Rating'], errors='coerce') >= 4].nlargest(3, 'Rating')
                    if len(positive_reviews) > 0:
                        st.subheader('✨ Positive Reviews')
                        for index, row in positive_reviews.iterrows():
                            comment = str(row['Comment'])[:80] + "..." if len(str(row['Comment'])) > 80 else str(row['Comment'])
                            st.markdown(f"⭐ {row['Rating']} - {comment}")
                except:
                    pass

                try:
                    # Display top negative comments with worst ratings
                    negative_reviews = product_data[pd.to_numeric(product_data['Rating'], errors='coerce') <= 2].nsmallest(3, 'Rating')
                    if len(negative_reviews) > 0:
                        st.subheader('💢 Negative Reviews')
                        for index, row in negative_reviews.iterrows():
                            comment = str(row['Comment'])[:80] + "..." if len(str(row['Comment'])) > 80 else str(row['Comment'])
                            st.markdown(f"⭐ {row['Rating']} - {comment}")
                except:
                    pass

                try:
                    # Display rating counts in different categories
                    st.subheader('Rating Counts')
                    rating_counts = pd.to_numeric(product_data['Rating'], errors='coerce').value_counts().sort_index(ascending=False)
                    if len(rating_counts) > 0:
                        for rating, count in rating_counts.items():
                            if pd.notna(rating):
                                st.write(f"🔹 Rating {rating} count: {int(count)}")
                except:
                    st.write("Unable to display rating counts")
