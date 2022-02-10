from decimal import Decimal, ROUND_HALF_UP


def calculate_payable_amt(hours: Decimal, hourly_rate: Decimal) -> Decimal:
    # use the hourly rate and hours to calculate pay
    # for currency we can use the Decimal.quantize method at the end of the calculation to handle rounding
    cents = Decimal('.01')
    payable_amt = (hours * hourly_rate).quantize(cents, ROUND_HALF_UP)
    return payable_amt
