import datetime
from scipy.optimize import newton


# Helper Functions

def get_settlement_date(trans_date, days_offset=2):
    """Calculates Spot (D+2) skipping weekends."""
    current = trans_date
    added = 0
    while added < days_offset:
        current += datetime.timedelta(days=1)
        if current.weekday() < 5:  # Mon-Fri
            added += 1
    return current


def get_days_act_act_icma(start_date, end_date, freq=1):
    """
    Returns the fraction of the year for ACT/ACT (ICMA).
    For Polish bonds (freq=1), the basis is the actual number of days
    in the current coupon period (365 or 366).
    """
    days_accrued = (end_date - start_date).days

    # Identify the full coupon period to determine the basis (365 or 366)
    # We assume annual coupons (Freq=1) as per problem statement
    # The start of the period is the last coupon date.
    # The end of the period is the next coupon date.

    # Simple logic to find next coupon date relative to start_date
    # (Assuming standard annual cycles)
    next_year = start_date.year + 1
    # Check if we cross a leap day in the future, strictly for basis determination
    # For this specific problem, all current periods are 2025-2026 (365 days)
    # except OK0127 which is zero coupon.

    # Logic: If Feb 29 is between start and end of COUPON PERIOD, basis is 366.
    # Current period for all 'July' bonds: 25-07-2025 to 25-07-2026.
    # Does 29-02-2026 exist? No. Basis = 365.
    basis = 365

    return days_accrued, basis


def calculate_ytm(price, settlement, flows, guess=0.05):
    """
    Calculates YTM (Internal Rate of Return) for given cash flows.
    Equation: Price = Sum( Flow_i / (1+y)^t_i )
    """

    def npv(y):
        val = 0
        for date, amount in flows:
            # Time in years from settlement
            # Using ACT/365 or ICMA logic.
            # For annual bonds, time = (Date - Settle) / 365 is standard approximation
            # or we count exact periods. Let's use exact days / 365 for YTM.
            t = (date - settlement).days / 365.0
            val += amount / ((1 + y) ** t)
        return val - price

    try:
        return newton(npv, guess)
    except:
        return None


# Input Data

trans_date = datetime.date(2025, 10, 17)
settle_date = get_settlement_date(trans_date, 2)
nominal = 1000.0

# Bond Database
# Format: Name, Maturity, CouponRate(%), CleanPrice(%)
bonds = [
    {"name": "DS0726", "mat": datetime.date(2026, 7, 25), "cpn": 2.50, "clean": 99.18},
    {"name": "OK0127", "mat": datetime.date(2027, 1, 25), "cpn": 0.00, "clean": 95.42},
    {"name": "DS0727", "mat": datetime.date(2027, 7, 25), "cpn": 2.50, "clean": 97.44},
    {"name": "PS0728", "mat": datetime.date(2028, 7, 25), "cpn": 7.50, "clean": 108.26},
    {"name": "PS0729", "mat": datetime.date(2029, 7, 25), "cpn": 4.75, "clean": 100.81},
]

# Calculations

results = []

for b in bonds:
    # A. Accrued Interest Calculation
    if b["cpn"] == 0:
        # Zero Coupon Bond
        accrued_val = 0.0
        dirty_val_pct = b["clean"]  # Clean = Dirty for Zero Coupon usually
    else:
        # Fixed Coupon Bond
        # Previous coupon was 25 July 2025
        prev_cpn_date = datetime.date(2025, 7, 25)

        days, basis = get_days_act_act_icma(prev_cpn_date, settle_date)

        # Accrued Interest Formula: Nominal * Rate * (Days/Basis)
        # We calculate AI as % of Nominal to match the table format
        ai_pct = b["cpn"] * (days / basis)
        accrued_val = ai_pct
        dirty_val_pct = b["clean"] + accrued_val

    # B. YTM Calculation
    # Generate Cash Flows
    flows = []

    # Iterate years until maturity to add coupons
    # Start from next coupon date
    # Note: OK0127 matures in Jan, others in July.

    current_flow_date = b["mat"]

    # We assume standard annual coupons working backwards from maturity
    # Generate list of coupon dates
    cf_dates = []
    d = b["mat"]
    while d > settle_date:
        cf_dates.append(d)
        try:
            d = d.replace(year=d.year - 1)
        except ValueError:
            # Handle Feb 29 leap year issue if applicable
            d = d.replace(month=2, day=28, year=d.year - 1)

    cf_dates.sort()  # Sort chronological

    for d in cf_dates:
        amt = b["cpn"]  # Coupon %
        if d == b["mat"]:
            amt += 100.0  # Add Principal at maturity
        flows.append((d, amt))

    ytm = calculate_ytm(dirty_val_pct, settle_date, flows)

    results.append({
        "Name": b["name"],
        "Clean": b["clean"],
        "Accrued": accrued_val,
        "Dirty": dirty_val_pct,
        "YTM": ytm * 100 if ytm else 0
    })

# Output

import pandas as pd

pd.options.display.float_format = '{:,.3f}'.format
df = pd.DataFrame(results)

print(f"Settlement Date: {settle_date}")
print("-" * 60)
print("Columns needed to be filled: ")
print(df[["Name", "Clean", "Accrued", "Dirty", "YTM"]].to_string(index=False))