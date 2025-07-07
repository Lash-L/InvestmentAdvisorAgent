import datetime
import os

import chromadb
from dotenv import load_dotenv
from newsapi import NewsApiClient


class NewsManager:
    """A class for managing news articles."""

    def __init__(self) -> None:
        """Initialize the NewsManager class."""
        load_dotenv()
        self._api = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])

    def get_industry_news(self, industry: str) -> dict:
        """Get news articles related to a specific industry.
        :param industry: The industry you want to search for.
        """
        response = self._api.get_everything(
            q=industry, language="en", page_size=25, sort_by="publishedAt"
        )
        return response

    def get_generic_investment_news(self) -> dict:
        """Get generic investment news based on some pre-filled queries."""
        response = self._api.get_everything(
            q="interest rates OR jobs report OR inflation OR market trends",
            language="en",
            page_size=50,
            sort_by="publishedAt",
        )
        return response


if __name__ == "__main__":
    # The idea would be that you would do this daily(or more frequently for all industries - store the results in a DB.
    # Then prune the DB of anything older than a week old. There is likely a better api than this. For POC of my agent,
    # I am simply doing this once.
    client = chromadb.PersistentClient(path="./news_db")
    collection = client.get_or_create_collection(name="news")
    INDUSTRIES = [
        "Consumer Electronics",
        "Software - Infrastructure",
        "Internet Content & Information",
        "Specialty Retail",
        "Auto - Manufacturers",
        "Semiconductors",
        "Internet Content & Information",
        "Asset Management",
    ]
    documents: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    for industry in INDUSTRIES:
        news = NewsManager().get_industry_news(industry)
        for article in news["articles"]:
            if article["url"] in ids:
                continue
            documents.append(
                f"Title: {article['title']}\nDescription: {article['description']}"
            )
            metadatas.append(
                {
                    "industry": industry,
                    "source_url": article["url"],
                    "published_ts": datetime.datetime.fromisoformat(
                        article["publishedAt"].replace("Z", "+00:00")
                    ).timestamp(),
                }
            )
            ids.append(article["url"])
    # For simplicity, just use chromadbs built in embedder.
    collection.add(ids, documents=documents, metadatas=metadatas)
