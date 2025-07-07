import datetime

import chromadb
from google.genai import types

from investmentadvisoragent.agent import Agent
from investmentadvisoragent.data.user_info import UserInfo


class MarketNewsAgent(Agent):
    """A agent who is responsible for providing news about the market that relate to their portfolio."""

    def __init__(self, user_info: UserInfo, agent_name: str, agent_model: str) -> None:
        """Initialize the MarketNewsAgent."""
        super().__init__(user_info, agent_name, agent_model)
        self._prompt = f"""
        Today's date is {datetime.datetime.today()}
        You are a financial assistant, your goal is to help a user understand how current news may impact their portfolio.
        This is the users portfolio:
        {[val.model_dump_json() for val in self._user_info.accounts.values()]}

        You have access to the following tool:
        1) News Finder: This will allow you to find news about a specific topic. Consider passing in broad queries that may relate opposed to just the stock ticker. i.e. for Apple, you could pass in ["Apple", "Technology"]

        Once you call the relevant tools, answer the user's query in a clear and concise way.

        """
        client = chromadb.PersistentClient(path="src/investmentadvisoragent/news_db")
        self._collection = client.get_collection(name="news")

    def query_news(
        self,
        query_texts: list[str],
        n_results: int = 5,
    ) -> list[dict]:
        """Find news articles related to a topic or industry via RAG.
        :param query_texts: List of search terms or topics to find relevant news articles.
        :param n_results: The maximum number of news articles to return.
        """
        db_res = self._collection.query(query_texts=query_texts, n_results=n_results)
        formatted_result = []
        for num_result in range(len(db_res["ids"])):
            for idx in db_res["ids"][num_result]:
                metadata = db_res["metadatas"][0][idx]
                document = db_res["documents"][0][idx]
                title = document.split("\nDescription: ")[0].replace("Title: ", "")
                description = document.split("\nDescription: ")[1]

                formatted_result.append(
                    {
                        "title": title,
                        "description": description,
                        "source_url": metadata["source_url"],
                        "industry": metadata["industry"],
                    }
                )

        return formatted_result

    @property
    def tools(self) -> list[types.Tool]:
        """Return the tools that the market news agent has access to."""

        def query_news(
            query_texts: list[str],
            n_results: int = 5,
        ) -> list[dict]:
            """Find news articles related to a topic or industry via RAG.
            :param query_texts: List of search terms or topics to find relevant news articles.
            :param n_results: The maximum number of news articles to return.
            """
            return self.query_news(query_texts, n_results)

        self._tools["query_news"] = query_news
        return [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="query_news",
                        response=news_tool_output_schema,
                        parameters=news_tool_schema,
                        description="Find news articles related to a topic or industry.",
                    )
                ]
            )
        ]


news_tool_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "query_texts": types.Schema(
            type=types.Type.ARRAY,
            description="List of search terms or topics to find relevant news articles.",
            items=types.Schema(type=types.Type.STRING),
        ),
        "n_results": types.Schema(
            type=types.Type.NUMBER,
            description="The maximum number of news articles to return.",
            default=5,
        ),
    },
    required=["query_texts"],
)
news_tool_output_schema = types.Schema(
    type=types.Type.ARRAY,
    description="A list of news articles that matched the user's query.",
    items=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "title": types.Schema(
                type=types.Type.STRING,
                description="The title of the news article.",
            ),
            "description": types.Schema(
                type=types.Type.STRING,
                description="A brief summary or description of the news article.",
            ),
            "source_url": types.Schema(
                type=types.Type.STRING,
                description="The URL link to the original source of the article.",
            ),
            "industry": types.Schema(
                type=types.Type.STRING,
                description="The industry category the article belongs to (e.g., 'Technology', 'Finance').",
            ),
        },
    ),
)
