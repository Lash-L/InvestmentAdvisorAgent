from google.genai import types

from investmentadvisoragent.agent import Agent
from investmentadvisoragent.company_manager import CompanyManager
from investmentadvisoragent.data.user_info import UserInfo
from investmentadvisoragent.generic_tools.account_diversification import (
    get_diversification,
)


class PortfolioAnalystAgent(Agent):
    """A agent who is responsible for analyzing the user's financial accounts."""

    def __init__(self, user_info: UserInfo, agent_name: str, agent_model: str) -> None:
        """Initialize the PortfolioAnalystAgent.
        :param user_info: The user's information.
        :param agent_name: The name to use for this agent
        :param agent_model: The model to use for this agent.
        """
        super().__init__(user_info, agent_name, agent_model)
        self._prompt = f"""
        You are responsible for analyzing the user's financial accounts.
        Their portfolio is:
        {[val.model_dump_json() for val in self._user_info.accounts.values()]}
        You have access to the following tools:
        1) Portfolio Diversification: This will allow you to analyze the diversification of the user's portfolio using
        HHI. Do NOT tell the user the HHI unless they specifically ask. Instead, dumb it down so that it is very easy
        for the user to understand. You can state things like percentages instead.

        Once you call the relevant tools, answer the user's query in a clear and concise way.
        """

    @property
    def tools(self) -> list[types.Tool]:
        """Return the tools that the portfolio analyst agent has access to."""
        diversification_tool = types.FunctionDeclaration(
            description="Calculate portfolio diversification. This will give back specific weights of each asset and the HHI.",
            name="get_portfolio_diversification",
        )

        def get_portfolio_diversification() -> dict:
            """Get the user's portfolio diversification."""
            # This is obviously wrong, just done for ease of showcasing this.
            company_manager = CompanyManager()
            company_info = {}
            for account in self._user_info.accounts.values():
                for asset in account.assets:
                    company_info[asset.identifier] = company_manager.get_profile(asset)
            return get_diversification(self._user_info, company_info)

        self._tools["get_portfolio_diversification"] = get_portfolio_diversification
        return [
            types.Tool(function_declarations=[diversification_tool]),
        ]
