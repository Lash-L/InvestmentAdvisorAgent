from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class AssetType(StrEnum):
    """Describe the type of asset - for now rather limited and not super used."""

    STOCK = "STOCK"
    BOND = "BOND"
    ETF = "ETF"


class Asset(BaseModel):
    """Describes a specific asset that the user owns."""

    identifier: str = Field(description="Unique identifier for the asset")
    amount: float = Field(
        description="Number of the asset that the user has (i.e. shares)"
    )
    asset_type: AssetType = Field(description="Type of the asset")
    purchase_date: datetime = Field(description="Date when the asset was purchased")
    purchase_price: float = Field(description="Price at which the asset was purchased")
    current_price: float | None = Field(description="Current price of the asset")
