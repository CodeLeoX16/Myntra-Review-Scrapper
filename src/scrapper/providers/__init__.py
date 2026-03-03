from __future__ import annotations

from src.scrapper.providers.myntra import MyntraReviewScraper


def get_scraper(platform: str, product_name: str, no_of_products: int):
    platform_norm = platform.strip().lower()

    if platform_norm in {"myntra"}:
        return MyntraReviewScraper(product_name=product_name, no_of_products=no_of_products)

    raise ValueError(
        f"Unsupported platform: {platform}. "
        f"Add a provider in src/scrapper/providers/ to support it."
    )


__all__ = ["get_scraper", "MyntraReviewScraper"]
