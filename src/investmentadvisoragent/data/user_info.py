from pydantic import BaseModel, Field

from .account import Account
from .property import Property


class UserInfo(BaseModel):
    """Describes the User's state."""

    name: str = Field(description="The name of the user")
    age: int = Field(description="The age of the user")
    accounts: dict[str, Account] = Field(description="The portfolio of the user")
    goals: list[str] = Field(description="The goals of the user")
    yearly_income: int = Field(description="The yearly income of the user")
    property: list[Property] = Field(description="The property of the user")
