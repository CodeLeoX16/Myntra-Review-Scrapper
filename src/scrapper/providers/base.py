from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseReviewScraper(ABC):
    """Base interface to support scraping multiple platforms."""

    @abstractmethod
    def get_review_data(self) -> pd.DataFrame:
        raise NotImplementedError
