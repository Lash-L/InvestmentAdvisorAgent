from google.genai import types


def calculate_compound_interest(
    current_amount: float,
    num_years: int,
    interest_rate: float,
    compounding_freq: int = 12,
    additional_monthly_contribution: float = 0,
) -> float:
    """Calculate the future value of an investment with regular contributions."""
    if interest_rate == 0:
        return current_amount + (
            additional_monthly_contribution * compounding_freq * num_years
        )

    future_value_principal = current_amount * (
        1 + interest_rate / compounding_freq
    ) ** (compounding_freq * num_years)

    # FV = M * [((1 + r/n)^(nt) - 1) / (r/n)]
    future_value_contributions = additional_monthly_contribution * (
        ((1 + interest_rate / compounding_freq) ** (compounding_freq * num_years) - 1)
        / (interest_rate / compounding_freq)
    )

    total_future_value = future_value_principal + future_value_contributions

    return total_future_value


interest_tool_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "current_amount": types.Schema(
            description="The amount that is currently in the account being compounded.",
            type=types.Type.NUMBER,
        ),
        "interest_rate": types.Schema(
            description="The rate at which this compounds",
            type=types.Type.NUMBER,
            default=0.08,
        ),
        "compounding_freq": types.Schema(
            description="The amount of times in a year that this should be compounded.",
            type=types.Type.NUMBER,
            default=12,
        ),
        "num_years": types.Schema(
            description="The number of years it will compound for",
            type=types.Type.NUMBER,
        ),
        "additional_monthly_contribution": types.Schema(
            description="An additional monthly contribution that the user wants to make",
            default=0,
        ),
    },
    required=["current_amount", "interest_rate", "num_years"],
)
