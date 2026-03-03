from src.exception import CustomException
from bs4 import BeautifulSoup as bs
import pandas as pd
import os, sys
import time
import shutil
from urllib.parse import quote


class ScrapeReviews:
    def __init__(self,
                 product_name:str,
                 no_of_products:int):
        # Lazy imports so Streamlit can boot even if Selenium isn't available
        # (e.g., dependency install issues on deployment platforms).
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        options = Options()

        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Streamlit Community Cloud runs on Linux where Chrome must be headless.
        # Keep Windows behavior unchanged.
        if os.name != "nt":
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            chrome_bin = os.environ.get("CHROME_BIN") or shutil.which("chromium") or shutil.which("chromium-browser")
            if chrome_bin:
                options.binary_location = chrome_bin

        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH") or shutil.which("chromedriver")
        
        # Start a new Chrome browser session
        service = Service(executable_path=chromedriver_path) if chromedriver_path else Service()
        self.driver = webdriver.Chrome(service=service, options=options)

        # Give dynamic pages time to render.
        self.driver.implicitly_wait(8)

        self.product_name = product_name
        self.no_of_products = no_of_products

    @staticmethod
    def _looks_blocked(page_source: str) -> bool:
        if not page_source:
            return False
        text = page_source.lower()
        return (
            "access denied" in text
            or "captcha" in text
            or "verify you are a human" in text
            or "request blocked" in text
        )

    def scrape_product_urls(self, product_name):
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            search_string = product_name.replace(" ","-")
            # no_of_products = int(self.request.form['prod_no'])

            encoded_query = quote(search_string)
            # Navigate to the URL
            self.driver.get(
                f"https://www.myntra.com/{search_string}?rawQuery={encoded_query}"
            )

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.results-base"))
            )

            myntra_text = self.driver.page_source
            if self._looks_blocked(myntra_text):
                raise Exception(
                    "Myntra blocked the request (captcha/access denied). "
                    "This often happens on Streamlit Cloud headless browsers. Try running locally."
                )
            myntra_html = bs(myntra_text, "html.parser")
            pclass = myntra_html.find_all("ul", {"class": "results-base"})

            product_urls = []
            for i in pclass:
                href = i.find_all("a", href=True)

                for product_no in range(len(href)):
                    t = href[product_no]["href"]
                    product_urls.append(t)

            return product_urls

        except Exception as e:
            raise CustomException(e, sys)

    def extract_reviews(self, product_link):
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            productLink = "https://www.myntra.com/" + product_link
            self.driver.get(productLink)
            prodRes = self.driver.page_source
            if self._looks_blocked(prodRes):
                raise Exception(
                    "Myntra blocked the request (captcha/access denied). "
                    "This often happens on Streamlit Cloud headless browsers. Try running locally."
                )

            # Wait for the product page to render key elements.
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "title"))
                )
            except Exception:
                pass

            prodRes_html = bs(prodRes, "html.parser")
            title_h = prodRes_html.find_all("title")

            self.product_title = title_h[0].text

            overallRating = prodRes_html.find_all(
                "div", {"class": "index-overallRating"}
            )
            for i in overallRating:
                self.product_rating_value = i.find("div").text
            price = prodRes_html.find_all("span", {"class": "pdp-price"})
            for i in price:
                self.product_price = i.text
            product_reviews = prodRes_html.find(
                "a", {"class": "detailed-reviews-allReviews"}
            )

            if not product_reviews:
                # Some pages lazy-load the reviews link. Try waiting briefly.
                try:
                    WebDriverWait(self.driver, 8).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a.detailed-reviews-allReviews"))
                    )
                    prodRes_html = bs(self.driver.page_source, "html.parser")
                    product_reviews = prodRes_html.find(
                        "a", {"class": "detailed-reviews-allReviews"}
                    )
                except Exception:
                    pass

            if not product_reviews:
                return None
            return product_reviews
        except Exception as e:
            raise CustomException(e, sys)
        
    def scroll_to_load_reviews(self):
        # Change the window size to load more data
        self.driver.set_window_size(1920, 1080)  # Example window size, adjust as needed

        # Get the initial height of the page
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Scroll in smaller increments, waiting between scrolls
        while True:
            # Scroll down by a small amount
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(3)  # Adjust this delay if needed
            
            # Calculate the new height after scrolling
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Break the loop if no new content is loaded after scrolling
            if new_height == last_height:
                break
            
            # Update the last height for the next iteration
            last_height = new_height



    def extract_products(self, product_reviews):
        try:
            t2 = product_reviews["href"]
            Review_link = "https://www.myntra.com" + t2
            self.driver.get(Review_link)
            
            self.scroll_to_load_reviews()
            
            review_page = self.driver.page_source

            review_html = bs(review_page, "html.parser")
            review = review_html.find_all(
                "div", {"class": "detailed-reviews-userReviewsContainer"}
            )

            user_rating = []
            user_comment = []
            user_name = []
            for i in review:
                user_rating = i.find_all(
                    "div", {"class": "user-review-main user-review-showRating"}
                )
                user_comment = i.find_all(
                    "div", {"class": "user-review-reviewTextWrapper"}
                )
                user_name = i.find_all("div", {"class": "user-review-left"})

            reviews = []
            for i in range(len(user_rating)):
                try:
                    rating = (
                        user_rating[i]
                        .find("span", class_="user-review-starRating")
                        .get_text()
                        .strip()
                    )
                except:
                    rating = "No rating Given"
                try:
                    comment = user_comment[i].text
                except:
                    comment = "No comment Given"
                try:
                    name = user_name[i].find("span").text
                except:
                    name = "No Name given"
                try:
                    date = user_name[i].find_all("span")[1].text
                except:
                    date = "No Date given"

                mydict = {
                    "Product Name": self.product_title,
                    "Over_All_Rating": self.product_rating_value,
                    "Price": self.product_price,
                    "Date": date,
                    "Rating": rating,
                    "Name": name,
                    "Comment": comment,
                }
                reviews.append(mydict)  #  a list of all dictionary elements

            review_data = pd.DataFrame(
                reviews,
                columns=[
                    "Product Name",
                    "Over_All_Rating",
                    "Price",
                    "Date",
                    "Rating",
                    "Name",
                    "Comment",
                ],
            )

            return review_data

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def skip_products(self, search_string, no_of_products, skip_index):
        product_urls: list = self.scrape_product_urls(product_name=search_string)

        product_urls.pop(skip_index)

    def get_review_data(self) -> pd.DataFrame:
        try:
            # search_string = self.request.form["content"].replace(" ", "-")
            # no_of_products = int(self.request.form["prod_no"])

            product_urls = self.scrape_product_urls(product_name=self.product_name)

            product_details = []

            review_len = 0

            while review_len < self.no_of_products and review_len < len(product_urls):
                product_url = product_urls[review_len]
                review = self.extract_reviews(product_url)

                if review:
                    product_detail = self.extract_products(review)
                    if product_detail is not None and not product_detail.empty:
                        product_details.append(product_detail)
                        review_len += 1
                    else:
                        product_urls.pop(review_len)
                else:
                    product_urls.pop(review_len)

            self.driver.quit()

            if not product_details:
                return pd.DataFrame(
                    columns=[
                        "Product Name",
                        "Over_All_Rating",
                        "Price",
                        "Date",
                        "Rating",
                        "Name",
                        "Comment",
                    ]
                )

            data = pd.concat(product_details, axis=0)
            
            data.to_csv("data.csv", index=False)
            
            return data   # For running Streamlit app, you can return the data as dataframe directly
                
            # For running Flask app, you can return the columns and values separately. Uncomment the following lines:

            # columns = data.columns

            # values = [[data.loc[i, col] for col in data.columns ] for i in range(len(data)) ]
            
            # return columns, values
        
    

        except Exception as e:
            raise CustomException(e, sys)
