# Investment Advisor Agent

A proof-of-concept system that demonstrates how an LLM can access and analyze a user's complete financial information to provide portfolio insights and financial guidance.

Note: This is just a PoC, I wanted to see if I could successfully get an agent that could do something like this. There are a lot of things I would do differently in a real system and this was just made in some free time i had over a couple of days.

## Overview

This agent is designed to help users understand their portfolio performance, identify areas of concern, and provide guidance on financial decisions. For legal reasons, it focuses on portfolio analysis and insights rather than providing strict financial advice.

The system performs best when provided with relevant financial data and tools (e.g., mortgage payoff calculators, compound interest calculators) rather than relying on the LLM to perform calculations independently.

Many parts of this system are done with static data and assumptions that would not be present in a real world system. Many things are simply engineered to work for this PoC opposed to being highly engineered.

In a real system you would want many more tools and all of the tools should be crafted with a financial advisor to ensure that the math and recommendations they are spitting out are accurate.

## Agent System

The system consists of four specialized agents:

1. **Investment Agent**: The main orchestrator that processes user input, routes requests to appropriate specialized agents, and returns comprehensive responses.

2. **Goal Planning Agent**: Assists users in reaching financial goals through compound interest calculations, mortgage payoff analysis, and other financial planning tools.

3. **Market News Agent**: Uses RAG (Retrieval-Augmented Generation) on pre-populated news data to provide relevant market insights. In production, this would use dynamic news feeds while maintaining RAG to optimize API costs.

4. **Portfolio Analyst**: Analyzes portfolio diversification, risk assessment, and provides insights on asset allocation.

# Example Queries

## Is there any relevant news on my stock holdings?

Here's a summary of recent news relevant to your stock holdings:

*   **Apple (AAPL):** Automakers are reportedly hesitant about Apple's new in-car interface, CarPlay Ultra.
*   **Amazon (AMZN):** Amazon has launched early Prime Day deals, particularly on its devices. Intuit is also introducing agents for QuickBooks, and Amazon is increasing its use of robots. Amazon is also noted as a top e-commerce stock to watch.
*   **Tesla (TSLA):** Tesla's sales in the UK have improved, with EVs accounting for 25% of new car sales in the first half of 2025. However, the UK's overall EV sales are below government targets, and internal combustion engine vehicles still dominate the Indian car market.
*   **NVIDIA (NVDA):** Some investment firms have recently altered their stakes in NVIDIA.
*   **ETFs:** The Invesco QQQ Trust (QQQ) has been identified as a "Promising Value Stock to Consider."

## How is my portfolio diversification?
Your Fidelity Roth IRA is well-diversified, with a good mix of ETFs and bonds, and is spread across different sectors. Your Schwab Brokerage account, however, is heavily concentrated in technology stocks, particularly AAPL. While this has likely led to significant gains, it also carries a higher risk.

Would you like me to analyze your holdings in more detail or perhaps suggest ways to diversify your Schwab account?

## What would be the impact of paying $200 more a month towards my mortgage opposed to putting $200 a month in the S&P 500?
Paying an extra \$200 per month towards your mortgage would allow you to pay it off 3 years and 3 months sooner, resulting in approximately $191,684.96 in interest savings.

Alternatively, investing that same \$200 per month into the S&P 500 could potentially grow to around $8,356.36 in three years, assuming a 10% annual interest rate.

## Future Improvements

There's a lot I would do if I spent some more time on this:
- Better databasing
- Actually get a large corpus of news that stays in for the last 7 days
- Add a bunch more functions
- Lots of prompt engineering