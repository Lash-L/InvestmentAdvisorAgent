from enum import StrEnum

from pydantic import BaseModel, Field

from .asset import Asset


class AccountType(StrEnum):
    """Describes the type of account - for now rather limited and not super used."""

    BROKERAGE = "BROKERAGE"
    ROTH_IRA = "ROTH"
    TRADITIONAL_IRA = "IRA"
    HSA = "HSA"


class RiskTolerance(StrEnum):
    """Describes the risk tolerance of the account - Not super used.."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Account(BaseModel):
    """Describes a specific account that the user owns."""

    name: str = Field(description="Name of the account")
    account_type: AccountType = Field(description="Type of the account")
    assets: list[Asset] = Field(description="Assets associated with the account")
    risk_tolerance: RiskTolerance = Field(description="Risk tolerance of the account")
