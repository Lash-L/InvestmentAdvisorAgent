from investmentadvisoragent.agents.investment_advisor import InvestmentAdvisorAgent
from investmentadvisoragent.examples import example_user

agent = InvestmentAdvisorAgent(
    user_info=example_user,
    agent_name="Investment Advisor",
    agent_model="gemini-2.5-flash-lite-preview-06-17",
)

while True:
    print(agent.chat(input("")))
