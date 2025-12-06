import math
import pandas as pd
from datetime import date, timedelta

# Helper: add business days (weekends only)
def add_business_days(d: date, n: int) -> date:
    """Add n business days to date d, skipping Sat/Sun."""
    step = 1 if n >= 0 else -1
    remaining = abs(n)
    cur = d
    while remaining > 0:
        cur += timedelta(days=step)
        if cur.weekday() < 5:  # 0=Monday ...... 4=Friday
            remaining -= 1
    return cur

# ACT/ACT (ICMA) fraction for annual coupons
def actact_icma_fraction(d1: date, d2: date, period_start: date, period_end: date) -> float:
    """
    Fraction between d1 and d2 using ACT/ACT(ICMA), for a single coupon period.
    For annual coupons: actual days / actual days in coupon period.
    """
    return (d2 - d1).days / (period_end - period_start).days

# Solve YTM from dirty price using bisection
def ytm_from_dirty_price(dirty_price: float, cashflows: list[tuple[float, float]], tol=1e-12, max_iter=200) -> float:
    """
    Solve for y in:
        dirty_price = sum CF_i / (1+y)^(t_i)
    cashflows: list of (t_i in years, CF_i in PLN)
    """
    def f(y: float) -> float:
        return sum(cf / ((1.0 + y) ** t) for t, cf in cashflows) - dirty_price

    lo, hi = -0.90, 1.00
    flo, fhi = f(lo), f(hi)

    # Expand bracket if needed
    expand = 0
    while flo * fhi > 0 and expand < 50:
        hi *= 2
        fhi = f(hi)
        expand += 1
    if flo * fhi > 0:
        raise ValueError("Could not bracket the root for YTM.")

    # Bisection
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if abs(fmid) < tol or (hi - lo) / 2 < tol:
            return mid
        if flo * fmid > 0:
            lo, flo = mid, fmid
        else:
            hi, fhi = mid, fmid
    return (lo + hi) / 2

# Bonds data (from the table in exercise 2)

trade_date = date(2025, 10, 17)
settlement = add_business_days(trade_date, 2)  # spot D+2 (weekends only)

N = 1000.0  # nominal PLN

bonds = [
    ("DS0726", date(2026, 7, 25), 0.0250, 99.18, (7, 25)),
    ("OK0127", date(2027, 1, 25), 0.0000, 95.42, (1, 25)),  # zero-coupon
    ("DS0727", date(2027, 7, 25), 0.0250, 97.44, (7, 25)),
    ("PS0728", date(2028, 7, 25), 0.0750, 108.26, (7, 25)),
    ("PS0729", date(2029, 7, 25), 0.0475, 100.81, (7, 25)),
]

def last_and_next_coupon(settle: date, coupon_mmdd: tuple[int, int]) -> tuple[date, date]:
    """Annual coupon on fixed (month,day): return last_coupon and next_coupon around settlement."""
    mm, dd = coupon_mmdd
    cand = date(settle.year, mm, dd)
    if cand >= settle:
        return date(settle.year - 1, mm, dd), cand
    else:
        return cand, date(settle.year + 1, mm, dd)

rows = []

for name, maturity, c, clean_pct, mmdd in bonds:
    coupon = N * c
    clean_pln = N * clean_pct / 100.0

    # Accrued interest (ACT/ACT ICMA) > only for coupon bonds
    if c == 0.0:
        accrued = 0.0
    else:
        last_cpn, next_cpn = last_and_next_coupon(settlement, mmdd)
        accrued_frac = actact_icma_fraction(last_cpn, settlement, last_cpn, next_cpn)
        accrued = coupon * accrued_frac

    dirty = clean_pln + accrued

    # Time to next coupon in "coupon periods": t1 = fraction (ACT/ACT ICMA), then +1 each year
    last_cpn, next_cpn = last_and_next_coupon(settlement, mmdd)
    period_len_days = (next_cpn - last_cpn).days
    t1 = (next_cpn - settlement).days / period_len_days

    # Build cashflows CF(t)
    cashflows = []
    if name == "OK0127":
        # Zero coupon: principal only at maturity; maturity is 1 full period after next coupon date
        cashflows.append((t1 + 1.0, N))
    else:
        # Coupon bond: coupons each year until maturity, last CF includes principal
        d = next_cpn
        k = 0
        while d <= maturity:
            t = t1 + k
            cf = coupon + (N if d == maturity else 0.0)
            cashflows.append((t, cf))
            d = date(d.year + 1, d.month, d.day)
            k += 1

    # YTM from dirty price
    y = ytm_from_dirty_price(dirty, cashflows)

    # Macaulay duration (use dirty price P) and Modified duration
    pv_list = [cf / ((1.0 + y) ** t) for t, cf in cashflows]
    P = sum(pv_list)
    D = sum(t * pv for (t, _), pv in zip(cashflows, pv_list)) / P
    MD = D / (1.0 + y)

    rows.append({
        "Bond": name,
        "Settlement (D+2)": settlement.isoformat(),
        "Accrued interest (PLN)": accrued,
        "Dirty price (PLN)": dirty,
        "YTM": y,
        "Macaulay duration (years)": D,
        "Modified duration (years)": MD,
    })

df = pd.DataFrame(rows)

# Print
out = df.copy()
out["Accrued interest (PLN)"] = out["Accrued interest (PLN)"].map(lambda x: f"{x:,.2f}")
out["Dirty price (PLN)"] = out["Dirty price (PLN)"].map(lambda x: f"{x:,.2f}")
out["YTM"] = out["YTM"].map(lambda x: f"{100*x:.4f}%")
out["Macaulay duration (years)"] = out["Macaulay duration (years)"].map(lambda x: f"{x:.6f}")
out["Modified duration (years)"] = out["Modified duration (years)"].map(lambda x: f"{x:.6f}")

print(out.to_string(index=False))


'''
Conclusion:

Duration increases with maturity: DS0726 has the lowest duration, while PS0729 has the highest, meaning longer bonds are more interest-rate sensitive.

The zero-coupon bond (OK0127) has Macaulay duration equal to time to maturity, because all value is received at redemption.

Modified Duration is slightly lower than Macaulay Duration (MD = D / (1 + y)), so it directly measures price sensitivity to yield changes.

PS0729 is the most sensitive to yield shifts (highest MD), whereas DS0726 is the least sensitive (lowest MD).

Higher coupon payments reduce duration compared to a similar-maturity lower-coupon/zero-coupon bond, since more cash is received earlier.
'''
