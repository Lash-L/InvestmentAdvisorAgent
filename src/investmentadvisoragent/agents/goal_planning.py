import datetime

from google.genai import types

from investmentadvisoragent.agent import Agent
from investmentadvisoragent.data.user_info import UserInfo
from investmentadvisoragent.generic_tools.ask_question_tool import (
    ask_question,
    question_schema,
)
from investmentadvisoragent.generic_tools.compound_interest import (
    calculate_compound_interest,
    interest_tool_schema,
)
from investmentadvisoragent.generic_tools.mortgage_payoff import (
    calculate_mortgage_payoff,
    mortgage_tool_schema,
)


class GoalPlanningAgent(Agent):
    """Help a user reach their specific goals."""

    def __init__(self, user_info: UserInfo, agent_name: str, agent_model: str) -> None:
        """Initialize the GoalPlanningAgent."""
        super().__init__(user_info, agent_name, agent_model)
        self._prompt = f"""
    Today's date is: {datetime.datetime.today()}
    You are a financial assistant, your goal is to help a user better understand their finances and what it will take to reach their goals.
    The User has the following information associated with them:
    {user_info.model_dump_json()}

    Use the user's portfolio to answer any questions they may have. Assume that is their entire financial picture unless stated otherwise.
    You have access to the following tools:
    1) Compound Interest Calculator: This will allow you to do calculations to figure out how an investment or debt will grow compoundly.
    2) Mortgage calculator: Determine when their mortgage will be paid off based on extra payments.
    3) Ask Question: Ask the user clarifying questions to help you solve either 1 or 2. If it makes sense, you should make assumptions for the answers instead of asking. But if there is something concrete that is needed, ask the user.
    Once you call the relevant tools, answer the user's query in a clear and concise way. Summarize what you did

    If the user asks for anything else, let them know that is not currently possible.
    """

        self._user_info = user_info

    @property
    def tools(self) -> list[types.Tool]:
        """Return the tools that the goal planning agent has access to."""
        interest_tool = types.FunctionDeclaration(
            description="Calculate compound interest",
            parameters=interest_tool_schema,
            name="calculate_compound_interest",
        )
        mortgage_tool = types.FunctionDeclaration(
            description="Calculate when the user's mortgage can be paid off",
            parameters=mortgage_tool_schema,
            name="mortgage_tool_schema",
        )
        question_tool = types.FunctionDeclaration(
            description="Ask a question to the user",
            parameters=question_schema,
            name="ask_question",
        )

        self._tools["calculate_compound_interest"] = calculate_compound_interest
        self._tools["mortgage_tool_schema"] = calculate_mortgage_payoff
        self._tools["ask_question"] = ask_question
        return [
            types.Tool(function_declarations=[interest_tool]),
            types.Tool(function_declarations=[mortgage_tool]),
            types.Tool(function_declarations=[question_tool]),
        ]
