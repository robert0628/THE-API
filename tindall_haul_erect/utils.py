from decimal import Decimal, ROUND_HALF_UP
from .models import UtilitiesBillingLookup, PreStressBillingLookup, UnloadingTimeLookup


def calculate_payable_amt(hours: Decimal, hourly_rate: Decimal) -> Decimal:
    # use the hourly rate and hours to calculate pay
    # for currency we can use the Decimal.quantize method at the end of the calculation to handle rounding
    cents = Decimal('.01')
    payable_amt = (hours * hourly_rate).quantize(cents, ROUND_HALF_UP)
    return payable_amt


def lookup_base_std(delivery_type: str, outbound_miles: int) -> tuple[Decimal, Decimal]:
    # Based on the delivery type lookup the base std hrs and amt that correspond to the outbound miles
    # use the either the UtilitiesBillingLookup table or PreStressBillingLookup table
    if delivery_type == "UTL":
        try:
            query = UtilitiesBillingLookup.objects.get(outbound_miles=outbound_miles)
            base_std_hrs = query.base_std_hrs
            base_std_amt = query.base_std_billable_amt
        except UtilitiesBillingLookup.DoesNotExist:
            base_std_hrs = Decimal("0.00")
            base_std_amt = Decimal("0.00")
    else:
        try:
            query = PreStressBillingLookup.objects.get(outbound_miles=outbound_miles)
            base_std_hrs = query.base_std_hrs
            base_std_amt = query.base_std_billable_amt
        except PreStressBillingLookup.DoesNotExist:
            base_std_hrs = Decimal("0.00")
            base_std_amt = Decimal("0.00")

    return base_std_hrs, base_std_amt


def lookup_addnl_std_hrs( delivery_type: str, pieces: str) -> Decimal:
    # Based on the delivery_type and pieces of the load lookup the addnl hrs
    # use the UnloadingTimeLookup table
    try:
        addnl_std_hrs = UnloadingTimeLookup.objects.get(delivery_type=delivery_type, pieces=pieces).addnl_std_hrs
    except UnloadingTimeLookup.DoesNotExist:
        addnl_std_hrs = Decimal("0.00")

    return addnl_std_hrs
