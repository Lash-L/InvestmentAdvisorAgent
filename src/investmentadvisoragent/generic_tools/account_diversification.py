from collections import defaultdict

from investmentadvisoragent.data.account import Account
from investmentadvisoragent.data.company_info import CompanyProfile
from investmentadvisoragent.data.user_info import UserInfo

# def get_hhi(weights: list[float]) -> float:
#     """Calculates the Herfindahl-Hirschman Index (HHI) for a list of weights.
#     """
#     return sum(weight**2 for weight in weights)


def get_account_diversification(
    account: Account, company_info: dict[str, CompanyProfile]
) -> dict:
    """Calculate the diversification of an account."""
    asset_values = defaultdict(float)
    sector_values = defaultdict(float)
    type_values = defaultdict(float)
    industry_values = defaultdict(float)

    for asset in account.assets:
        val = asset.current_price * asset.amount
        asset_values[asset.identifier] += val
        sector_values[company_info[asset.identifier].sector] += val
        type_values[asset.asset_type] += val
        industry_values[company_info[asset.identifier].industry] += val

    total_portfolio_value = sum(asset_values.values())

    asset_values = {
        name: value / total_portfolio_value for name, value in asset_values.items()
    }
    sector_values = {
        name: value / total_portfolio_value for name, value in sector_values.items()
    }
    type_values = {
        name: value / total_portfolio_value for name, value in type_values.items()
    }
    industry_values = {
        name: value / total_portfolio_value for name, value in industry_values.items()
    }

    return {
        "asset_distribution": asset_values,
        "sector_distribution": sector_values,
        "type_distribution": type_values,
        "industry_distribution": industry_values,
        # Removed HHI for now to keep things simple.
        # "asset_hhi": get_hhi(to_percentages(asset_values)),
        # "sector_hhi": get_hhi(to_percentages(sector_values)),
        # "type_hhi": get_hhi(to_percentages(type_values)),
        # "industry_hhi": get_hhi(to_percentages(industry_values)),
    }


def get_diversification(
    user_info: UserInfo, company_info: dict[str, CompanyProfile]
) -> dict:
    """Calculate the diversification of a user's portfolio."""
    # TODO: Handle the concept of multiple similar accounts (i.e. two brokerages)
    account_diversifications = {}
    for account in user_info.accounts.values():
        account_diversifications[account.name] = get_account_diversification(
            account, company_info
        )
    return account_diversifications
