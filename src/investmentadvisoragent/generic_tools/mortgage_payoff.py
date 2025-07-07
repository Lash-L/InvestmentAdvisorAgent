import math

from google.genai import types


def _calculate_payoff_months(
    principal: float, monthly_rate: float, monthly_payment: float
) -> float:
    """Calculate the number of months to pay off a loan.
    :param principal: The initial loan amount.
    :param monthly_rate: The monthly interest rate.
    :param monthly_payment: The monthly payment.
    """
    num_months = -math.log(
        1 - (principal * monthly_rate) / monthly_payment
    ) / math.log1p(monthly_rate)
    return num_months


def calculate_mortgage_payoff(
    principal: float,
    annual_interest_rate: float,
    monthly_payment: float,
    extra_monthly_payment: float = 0.0,
) -> dict:
    """Calculate mortgage payoff details with and without an extra payment.
    :param principal: The initial loan amount.
    :param annual_interest_rate: The annual interest rate (e.g., 0.05 for 5%).
    :param monthly_payment: The regular monthly payment
    :param extra_monthly_payment: The additional amount paid each month.
    """
    monthly_rate = annual_interest_rate / 12
    result: dict = {}

    original_months = _calculate_payoff_months(principal, monthly_rate, monthly_payment)

    original_total_interest = (monthly_payment * original_months) - principal
    result["original_payoff"] = {
        "payoff_time": f"{original_months} months",
        "total_interest_paid": round(original_total_interest, 2),
    }

    if extra_monthly_payment <= 0:
        return result

    total_monthly_payment = monthly_payment + extra_monthly_payment
    accelerated_months = _calculate_payoff_months(
        principal, monthly_rate, total_monthly_payment
    )

    accelerated_total_interest = (
        total_monthly_payment * accelerated_months
    ) - principal
    result["accelerated_payoff"] = {
        "payoff_time": f"{accelerated_months} months",
        "total_interest_paid": round(accelerated_total_interest, 2),
    }

    interest_saved = original_total_interest - accelerated_total_interest
    time_saved = original_months - accelerated_months
    result["summary"] = {
        "interest_saved": round(interest_saved, 2),
        "paid_off_sooner_by": f"{time_saved} months",
    }

    return result


mortgage_tool_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "principal": types.Schema(
            description="The current remaining principal balance of the mortgage.",
            type=types.Type.NUMBER,
        ),
        "annual_interest_rate": types.Schema(
            description="The annual interest rate of the mortgage (e.g., 0.05 for 5%).",
            type=types.Type.NUMBER,
        ),
        "monthly_payment": types.Schema(
            description="The regular required monthly payment (principal and interest).",
            type=types.Type.NUMBER,
        ),
        "extra_monthly_payment": types.Schema(
            description="Any additional amount to be paid each month towards the principal.",
            type=types.Type.NUMBER,
            default=0.0,
        ),
    },
    required=["principal", "annual_interest_rate", "monthly_payment"],
)
