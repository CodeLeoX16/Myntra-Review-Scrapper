from __future__ import annotations

import argparse
import time

from src.cloud_io import MongoIO
from src.nlp import add_sentiment_columns
from src.scrapper.scrape import ScrapeReviews


def run_once(product: str, count: int) -> None:
    scrapper = ScrapeReviews(product_name=product, no_of_products=count)
    df = scrapper.get_review_data()
    if df is None or len(df) == 0:
        print("No data scraped.")
        return

    df = add_sentiment_columns(df, text_column="Comment")

    mongo = MongoIO()
    mongo.store_reviews(product_name=product, reviews=df)
    print(f"Stored {len(df)} rows into MongoDB for product: {product!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Myntra scraping on a schedule and store results to MongoDB.")
    parser.add_argument("--product", required=True, help="Product search string")
    parser.add_argument("--count", type=int, default=1, help="Number of products to scrape")
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=0,
        help="Run repeatedly every N minutes (0 means run once)",
    )
    args = parser.parse_args()

    if args.interval_minutes <= 0:
        run_once(args.product, args.count)
        return

    while True:
        start = time.time()
        try:
            run_once(args.product, args.count)
        except Exception as exc:
            print(f"Scheduled run failed: {exc}")

        elapsed = time.time() - start
        sleep_seconds = max(0, args.interval_minutes * 60 - elapsed)
        print(f"Sleeping for {sleep_seconds:.0f}s...")
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    main()
