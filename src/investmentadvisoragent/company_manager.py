import json
import os

import fmpsdk
from dotenv import load_dotenv

from investmentadvisoragent.data.asset import Asset
from investmentadvisoragent.data.company_info import CompanyProfile

# Again a bad way to store a file, but fine for a PoC
DB_FILE = "src/investmentadvisoragent/company_profiles.json"


class CompanyManager:
    """A class for managing company profiles."""

    def __init__(self) -> None:
        """Initialize the CompanyManager class."""
        load_dotenv()

        self._fmp_api_key = os.environ.get("FMP_API")
        self._company_profiles: dict[str, CompanyProfile] = {}
        self._load_from_db()

    def get_profile(self, asset: Asset) -> CompanyProfile:
        """Get the company profile for a specific asset.
        :param asset: The asset you want to get the company profile for.
        """
        ticker = asset.identifier
        if ticker not in self._company_profiles:
            res = fmpsdk.company_profile(self._fmp_api_key, ticker)[0]
            self._company_profiles[ticker] = CompanyProfile(
                company_name=res["companyName"],
                description=res["description"],
                industry=res["industry"],
                sector=res["sector"],
                ticker=ticker,
            )
        return self._company_profiles[ticker]

    def _load_from_db(self) -> None:
        """Load the company profiles from the JSON database file on startup."""
        try:
            with open(DB_FILE) as f:
                data = json.load(f)
                for ticker, profile_data in data.items():
                    self._company_profiles[ticker] = CompanyProfile(
                        **json.loads(profile_data)
                    )
            print(
                f"Successfully loaded {len(self._company_profiles)} profiles from db."
            )
        except Exception:
            print("No db yet...")

    def save_to_db(self) -> None:
        """Save the current dictionary of company profiles to a JSON file."""
        print(f"Saving {len(self._company_profiles)} profile(s) to '{DB_FILE}'...")
        serializable_profiles = {
            ticker: profile.model_dump_json()
            for ticker, profile in self._company_profiles.items()
        }
        with open(DB_FILE, "w") as f:
            json.dump(serializable_profiles, f, indent=4)


if __name__ == "__main__":
    # This should be more dynamic. But for POC, just doing it once so that I can easily have the results
    # As I am attempting to showcase the agent, not this.
    company_manager = CompanyManager()
    from investmentadvisoragent.examples import (
        example_brokerage_account,
        example_roth_ira_account,
    )

    for asset in example_brokerage_account.assets:
        company_manager.get_profile(asset)
    for asset in example_roth_ira_account.assets:
        company_manager.get_profile(asset)
    company_manager.save_to_db()
