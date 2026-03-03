from __future__ import annotations

import pandas as pd

from src.scrapper.providers.base import BaseReviewScraper
from src.scrapper.scrape import ScrapeReviews


class MyntraReviewScraper(BaseReviewScraper):
    def __init__(self, product_name: str, no_of_products: int):
        self._impl = ScrapeReviews(product_name=product_name, no_of_products=no_of_products)

    def get_review_data(self) -> pd.DataFrame:
        return self._impl.get_review_data()
