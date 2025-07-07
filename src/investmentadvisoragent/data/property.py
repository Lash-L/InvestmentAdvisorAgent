from datetime import datetime

from pydantic import BaseModel, Field


class Property(BaseModel):
    """Describes the property that the user owns."""

    location: str = Field(description="The location of the property")
    purchase_price: float = Field(description="The purchase price of the property")
    fair_market_value: float = Field(
        description="The fair market value of the property"
    )
    loan_start_date: datetime = Field(description="The date when the loan was granted")
    loan_length: int = Field(description="The length of the loan in months")
    remaining_loan_balance: float = Field(description="The remaining loan balance")
    interest_rate: float = Field(description="The interest rate of the loan")
