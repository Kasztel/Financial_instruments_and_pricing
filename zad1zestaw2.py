import datetime
import pandas as pd


# Helper functions for date logic

def is_last_day_of_feb(d):
    """
    Check if a date is the end of February.
    Crucial for 30/360 US because the rule says:
    'If D1 is the last day of Feb, it changes to 30.'
    This handles both Feb 28 (non-leap) and Feb 29 (leap).
    """
    if d.month != 2: return False
    # If tomorrow is March, then today is the last day of Feb.
    next_day = d + datetime.timedelta(days=1)
    return next_day.month == 3


def get_days_30_360_us(d1, d2):
    """
    Logic for 30/360 US (NASD).
    Thinking process:
    1. Check if start date (D1) is end-of-Feb -> adjust to 30.
    2. Check if end date (D2) is end-of-Feb -> ONLY adjust to 30 if D1 was also adjusted.
    3. Standard 31st adjustments.
    """
    day1, m1, y1 = d1.day, d1.month, d1.year
    day2, m2, y2 = d2.day, d2.month, d2.year

    # Special Rule: End of February adjustments
    if m1 == 2 and is_last_day_of_feb(d1):
        day1 = 30
    if m2 == 2 and is_last_day_of_feb(d2) and day1 == 30:
        day2 = 30

    # Standard Rule: 31st becomes 30th
    if day2 == 31 and day1 >= 30: day2 = 30
    if day1 == 31: day1 = 30

    return (y2 - y1) * 360 + (m2 - m1) * 30 + (day2 - day1)


def get_days_30e_360(d1, d2):
    """
    Logic for 30E/360 (Eurobond).
    This is simpler than US.
    Rule: Just treat 31st as 30th.
    Feb 28/29 usually stays as is.
    """
    day1, m1, y1 = d1.day, d1.month, d1.year
    day2, m2, y2 = d2.day, d2.month, d2.year

    if day1 == 31: day1 = 30
    if day2 == 31: day2 = 30

    return (y2 - y1) * 360 + (m2 - m1) * 30 + (day2 - day1)


def get_settlement_date(trans_date, days_offset=2):
    """
    Calculates Spot Date (T+2).
    Assignment warning: "Remember about weekends!"

    Logic:
    - Start at transaction date.
    - Loop until we have added 2 'business' days.
    - If it's Sat/Sun, don't count it.
    """
    current = trans_date
    added = 0
    while added < days_offset:
        current += datetime.timedelta(days=1)
        # Python: 0=Monday, ..., 5=Saturday, 6=Sunday
        if current.weekday() < 5:  # Only count if it's a weekday
            added += 1
    return current



nominal = 10000.0
rate = 0.10
base_coupon = nominal * rate  # 1000 EUR
clean_price = 9980.00  # 99.80% of 10,000

conventions = ["30/360 US", "30E/360", "ACT/ACT (ICMA)", "ACT/365 (Fixed)"]

# Part A: Value of Coupons ---
# "Compute the value of coupons paid in 2024, 2025 and 2026."

# Thinking:
# Usually, coupons are fixed (1000 EUR).
# But if we strictly apply day counts (like ACT/365), a Leap Year
# might result in a slightly higher payment (366/365).
# Let's calculate exactly to be safe.

periods = [
    # (Year Paid, Period Start, Period End)
    # 2024 is a Leap Year, so the period covers 29th Feb.
    (2024, datetime.date(2023, 2, 28), datetime.date(2024, 2, 29)),
    (2025, datetime.date(2024, 2, 29), datetime.date(2025, 2, 28)),
    (2026, datetime.date(2025, 2, 28), datetime.date(2026, 2, 28))
]

table_a_data = []

for conv in conventions:
    row = [conv]
    for year, start, end in periods:

        if conv == "ACT/365 (Fixed)":
            # Strict Interpretation:
            # Days in period / 365.
            # In a leap year, this is 366/365 > 1.0
            num = (end - start).days
            denom = 365
            val = base_coupon * (num / denom)

        elif conv == "ACT/ACT (ICMA)":
            # ICMA Rule: Coupon is paid annually, so period is exactly 1.0.
            val = base_coupon

        else:  # 30/360 variations
            # 30/360 assumes every year is 360 days.
            # So a full year is always 360/360 = 1.0.
            val = base_coupon

        row.append(val)
    table_a_data.append(row)

df_a = pd.DataFrame(table_a_data, columns=["Convention", "Coupon 2024", "Coupon 2025", "Coupon 2026"])

# Part B: Transaction Values

trans_date = datetime.date(2025, 10, 17)  # Friday
settle_date = get_settlement_date(trans_date, 2)

# CHECK: Since T is Friday, T+1 is Monday, T+2 is Tuesday.
# Date gap is 4 days. Correct.

prev_cpn_date = datetime.date(2025, 2, 28)  # Last coupon paid
next_cpn_date = datetime.date(2026, 2, 28)  # Next coupon due

table_b_data = []

for conv in conventions:
    # 1. Calculate Days Accrued (Numerator)
    if conv == "30/360 US":
        days = get_days_30_360_us(prev_cpn_date, settle_date)
        basis = 360
    elif conv == "30E/360":
        days = get_days_30e_360(prev_cpn_date, settle_date)
        basis = 360
    elif conv == "ACT/ACT (ICMA)":
        days = (settle_date - prev_cpn_date).days
        # ICMA Denominator is actual days in the CURRENT coupon year
        basis = (next_cpn_date - prev_cpn_date).days
    elif conv == "ACT/365 (Fixed)":
        days = (settle_date - prev_cpn_date).days
        basis = 365

    # 2. Calculate Accrued Interest
    # Formula: Coupon * (Days / Basis)
    accrued = base_coupon * (days / basis)

    # 3. Calculate Dirty Price (Cash Flow)
    # Dirty = Clean Price + Accrued
    dirty = clean_price + accrued

    table_b_data.append([conv, days, basis, accrued, dirty])

df_b = pd.DataFrame(table_b_data, columns=["Convention", "Days Accrued", "Basis", "Accrued Int", "Dirty Price"])

# Display Results 

pd.options.display.float_format = '{:,.2f}'.format

print(f"Transaction Date: {trans_date} (Friday)")
print(f"Settlement Date:  {settle_date} (Tuesday -> 'D+4' rule applies)")
print(f"Nominal: {nominal}, Coupon Rate: {rate * 100}%")
print("=" * 60)
print("Table A: Value of Coupons (EUR)")
print("Note: ACT/365 shows >1000 in 2024 because of the leap day.")
print("-" * 60)
print(df_a.to_string(index=False))
print("\n" + "=" * 60)
print("Table B: Transaction Values (EUR)")
print("Note: 30/360 US vs 30E/360 differ on how they handle Feb 28.")
print("-" * 60)
print(df_b.to_string(index=False))