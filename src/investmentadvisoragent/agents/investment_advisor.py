from google.genai import types

from investmentadvisoragent.agent import Agent
from investmentadvisoragent.agents.goal_planning import GoalPlanningAgent
from investmentadvisoragent.agents.market_news_agent import MarketNewsAgent
from investmentadvisoragent.agents.portfolio_analyst import PortfolioAnalystAgent
from investmentadvisoragent.data.user_info import UserInfo


class InvestmentAdvisorAgent(Agent):
    """The main agent that is responsible for routing the user to the right agent."""

    def __init__(self, user_info: UserInfo, agent_name: str, agent_model: str) -> None:
        """Initialize the InvestmentAdvisorAgent."""
        super().__init__(user_info, agent_name, agent_model)
        self._goal_planning_agent = GoalPlanningAgent(
            user_info,
            agent_name="Goal Planner",
            agent_model="gemini-2.5-flash-lite-preview-06-17",
        )
        self._market_news_agent = MarketNewsAgent(
            user_info,
            agent_name="Market News",
            agent_model="gemini-2.5-flash",
        )
        self._portfolio_analyst_agent = PortfolioAnalystAgent(
            user_info,
            agent_name="Portfolio Analyst",
            agent_model="gemini-2.5-flash-lite-preview-06-17",
        )

        self._prompt = """
        You are a investment assistant! Your goal is to help a user getting a better understanding of their financial
        status.

        You are responsible for routing the user to the right agent.
        The other agents are:
        1) Goal Planning Agent - This agent is responsible for helping a user reach their specific goals. (compounding interest, mortage payoff, etc.)
        2) Market News Agent - This agent is responsible for providing news about the market that relate to their portfolio.
        3) Portfolio Analyst Agent - This agent is responsible for Analyzing the user's financial accounts.

        Call whatever combination of agents that are needed to help the user. Then combine the data and respond in a clear and concise manner.
        If a user asks you to do a task that is not covered by any of the agents, you should respond with:
        I am sorry, I do not know how to help you with that.
        """

    @property
    def tools(self) -> list[types.Tool]:
        """Return the tools - aka the other agents - that the investment advisor agent has access to."""
        input_schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "prompt": types.Schema(
                    type=types.Type.STRING,
                    description="The prompt that should be given to the agent. You can modify the user's prompt slightly to give more context if needed.",
                )
            },
        )
        market_news_agent = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="market_news_agent",
                    parameters=input_schema,
                    description="This agent is responsible for providing news about the market that relate to their portfolio",
                )
            ]
        )
        goal_planning_agent = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="goal_planning_agent",
                    parameters=input_schema,
                    description="This agent is responsible for helping a user reach their specific goals",
                )
            ]
        )
        portfolio_analyst_agent = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="portfolio_analyst_agent",
                    parameters=input_schema,
                    description="This agent is responsible for Analyzing the user's financial accounts",
                )
            ]
        )

        def market_news_fn(prompt: str) -> dict:
            """Call the market news agent."""
            return {"response": self._market_news_agent.chat(prompt)}

        self._tools["market_news_agent"] = market_news_fn

        def goal_planning_fn(prompt: str) -> dict:
            """Call the goal planning agent."""
            return {"response": self._goal_planning_agent.chat(prompt)}

        self._tools["goal_planning_agent"] = goal_planning_fn

        def portfolio_analyst_fn(prompt: str) -> dict:
            """Call the portfolio analyst agent."""
            return {"response": self._portfolio_analyst_agent.chat(prompt)}

        self._tools["portfolio_analyst_agent"] = portfolio_analyst_fn
        return [market_news_agent, goal_planning_agent, portfolio_analyst_agent]
