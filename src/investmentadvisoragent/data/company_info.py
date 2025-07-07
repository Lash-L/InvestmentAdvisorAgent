from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    """Describes the company profile."""

    company_name: str = Field(description="The official name of the company.")
    description: str = Field(
        description="A summary of the company's business and operations."
    )
    industry: str = Field(description="The specific industry the company operates in.")
    sector: str = Field(description="The broader market sector the company belongs to.")
    ticker: str = Field(description="The stock market ticker symbol of the company.")
