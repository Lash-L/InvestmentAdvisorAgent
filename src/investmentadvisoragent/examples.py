# Synthetic example data
from datetime import datetime

from src.investmentadvisoragent.data import (
    Account,
    AccountType,
    Asset,
    AssetType,
    Property,
    RiskTolerance,
    UserInfo,
)

example_brokerage_account = Account(
    name="Schwab Brokerage #2124",
    account_type=AccountType.BROKERAGE,
    assets=[
        Asset(
            identifier="AAPL",
            purchase_date=datetime(2022, 10, 25),
            purchase_price=145.09,
            amount=5000,  # To simulate being poorly diversified in a specific asset.
            asset_type=AssetType.STOCK,
            current_price=212.94,
        ),
        Asset(
            identifier="MSFT",
            purchase_date=datetime(2023, 8, 15),
            purchase_price=301.78,
            amount=35,
            asset_type=AssetType.STOCK,
            current_price=497.37,
        ),
        Asset(
            identifier="GOOGL",
            purchase_date=datetime(2023, 2, 10),
            purchase_price=125.46,
            amount=40,
            asset_type=AssetType.STOCK,
            current_price=177.53,
        ),
        Asset(
            identifier="AMZN",
            purchase_date=datetime(2023, 1, 20),
            purchase_price=119.57,
            amount=25,
            asset_type=AssetType.STOCK,
            current_price=223.42,
        ),
        Asset(
            identifier="TSLA",
            purchase_date=datetime(2024, 3, 4),
            purchase_price=230.14,
            amount=15,
            asset_type=AssetType.STOCK,
            current_price=293.46,
        ),
        Asset(
            identifier="NVDA",
            purchase_date=datetime(2025, 2, 20),
            purchase_price=121.50,
            amount=60,
            asset_type=AssetType.STOCK,
            current_price=158.31,
        ),
        Asset(
            identifier="META",
            purchase_date=datetime(2025, 5, 10),
            purchase_price=495.70,
            amount=20,
            asset_type=AssetType.STOCK,
            current_price=723.23,
        ),
    ],
    risk_tolerance=RiskTolerance.HIGH,
)

# Roth IRA account with ETFs
example_roth_ira_account = Account(
    name="Fidelity Roth IRA #5581",
    account_type=AccountType.ROTH_IRA,
    assets=[
        Asset(
            identifier="VTI",
            purchase_date=datetime(2023, 1, 5),
            purchase_price=208.95,
            amount=20,
            asset_type=AssetType.ETF,
            current_price=307.04,
        ),
        Asset(
            identifier="VTI",
            purchase_date=datetime(2025, 1, 15),
            purchase_price=268.40,
            amount=10,
            asset_type=AssetType.ETF,
            current_price=307.04,
        ),
        Asset(
            identifier="VXUS",
            purchase_date=datetime(2023, 1, 5),
            purchase_price=52.30,
            amount=50,
            asset_type=AssetType.ETF,
            current_price=69.05,
        ),
        Asset(
            identifier="BND",
            purchase_date=datetime(2023, 1, 15),
            purchase_price=73.68,
            amount=30,
            asset_type=AssetType.BOND,
            current_price=72.94,
        ),
        Asset(
            identifier="SCHD",
            purchase_date=datetime(2022, 7, 22),
            purchase_price=71.44,
            amount=40,
            asset_type=AssetType.ETF,
            current_price=27.27,
        ),
        Asset(
            identifier="QQQ",
            purchase_date=datetime(2025, 3, 1),
            purchase_price=435.60,
            amount=15,
            asset_type=AssetType.ETF,
            current_price=553.32,
        ),
    ],
    risk_tolerance=RiskTolerance.MEDIUM,
)

example_user = UserInfo(
    name="Luke Skywalker",
    age=32,
    accounts={
        "Brokerage": example_brokerage_account,
        "Roth": example_roth_ira_account,
    },
    yearly_income=100000,
    goals=["I want to payoff my house within 3 years", "I want to retire when i am 55"],
    property=[
        Property(
            location="San Francisco",
            purchase_price=1000000,
            fair_market_value=1100000,
            loan_start_date=datetime(2023, 1, 1),
            remaining_loan_balance=900000,
            loan_length=30 * 12,
            interest_rate=0.08,
        )
    ],
)
