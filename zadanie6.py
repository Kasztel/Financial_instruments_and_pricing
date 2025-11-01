"""
We compare three deposit setups over 12 months with monthly compounding.

Notation:
- r is a 'nominal annual' rate (decimal), e.g., 6.5% p.a. -> r = 0.065.
- With monthly compounding, a nominal annual rate r implies a monthly factor of (1 + r/12).
- For a schedule of month-specific nominal annual rates r_i (i = 1..12), the i-th month's
  factor is (1 + r_i/12).

Formulas used:
1) Effective annual rate (EAR) for a 'variable' schedule (r_1,...,r_12):
       EAR = product_{i=1..12} (1 + r_i/12) - 1
   Rationale: multiply all monthly growth factors; subtract 1 to convert factor to "rate".
   Note: order does not matter (multiplication is commutative), so rising 1..12% equals falling 12..1%.

2) Effective annual rate (EAR) for a 'constant' nominal annual rate r with monthly compounding:
       EAR = (1 + r/12)^12 - 1

3) Monthly payout case (no addition to principal):
   The payout in month i equals: principal * (r_i/12).
   Over 12 months, the *sum* of payouts (without reinvestment) equals:
       principal * ( (r_1 + ... + r_12) / 12 )
   i.e., principal times the arithmetic mean nominal rate.

4) Future value (FV) of monthly payouts if they are reinvested externally to the year-end:
   Assume you receive cash at the *end* of month k, then reinvest it monthly at rate m
   for (12 - k) months. Then:
       FV = sum_{k=1..12} [ cashflow_k * (1 + m)^(12 - k) ]
   This is for illustration only; it shows the timing effect (earlier cash is better).
"""

from typing import List

def ear_variable_schedule(r_list: List[float]) -> float:
    # EAR for variable monthly nominal rates
    # uses formula (1): EAR = product (1 + r_i/12) - 1
    factor = 1.0
    for r in r_list:
        # monthly compounding when month i has nominal annual rate r:
        # monthly factor = (1 + r/12)
        factor *= (1.0 + r/12.0)
    # convert the 12-month factor into an effective annual rate by subtracting 1
    return factor - 1.0

def ear_constant(r: float) -> float:
    # EAR for a constant nominal annual rate r compounded monthly
    # uses formula (2): EAR = (1 + r/12)^12 - 1
    return (1.0 + r/12.0)**12 - 1.0

def monthly_cashflows(r_list: List[float], principal: float = 1.0) -> List[float]:
    # monthly interest payouts with no addition to principal
    # uses formula (3): month i pays principal * (r_i/12)
    # return the list of 12 such payouts (one per month)
    return [principal * (r/12.0) for r in r_list]

def future_value_of_monthly_cf(cashflows: List[float], monthly_rate: float) -> float:
    # future value at year end if monthly payouts are reinvested monthly at rate m
    # uses formula (4): FV = sum_{k=1.....12} cash_k * (1 + m)^(12 - k)
    FV = 0.0
    for k, c in enumerate(cashflows, start=1):
        # cash c arrives at end of month k, so it compounds for (12 - k) months
        FV += c * (1.0 + monthly_rate)**(12 - k)
    return FV

if __name__ == "__main__":
    # A: rising schedule (month-specific nominal annual rates)
    rates_A = [i/100.0 for i in range(1, 13)]  # 1%, 2%, ..., 12% (rising)
    # C: falling schedule 
    rates_C = list(reversed(rates_A))          # 12%, ..., 1% (falling)
    # B: constant nominal annual rate 6.5% with monthly compounding
    r_B = 0.065

    # part a: compute effective annual rates (EAR) using monthly compounding to principal
    ear_A = ear_variable_schedule(rates_A)     # formula (1)
    ear_C = ear_variable_schedule(rates_C)     # equals ear_A by product commutativity
    ear_B = ear_constant(r_B)                  # formula (2)

    print("Part (a): Effective annual rates (EAR) [%]")
    print("A (rising 1%->12%): {:.6f}".format(100*ear_A))
    print("B (constant 6.5%): {:.6f}".format(100*ear_B))
    print("C (falling 12%->1%): {:.6f}".format(100*ear_C))

    # part b: monthly payouts (no reinvestment to the principal)
    P = 1.0
    # each month i pays P * (r_i/12)
    cf_A = monthly_cashflows(rates_A, P)
    cf_B = monthly_cashflows([r_B]*12, P)      # same payout each month for the constant rate
    cf_C = monthly_cashflows(rates_C, P)

    print("\nPart (b): Sum of monthly payouts over the year (per P=1)")
    # sums should be equal across A, B, C because all share the same average nominal rate (6.5%)
    print("A: {:.8f}".format(sum(cf_A)))
    print("B: {:.8f}".format(sum(cf_B)))
    print("C: {:.8f}".format(sum(cf_C)))

    # optional illustration: reinvest the monthly payouts to year-end at 6.5% p.a. (monthly rate m)
    m = 0.065/12.0
    fv_A = future_value_of_monthly_cf(cf_A, m)
    fv_B = future_value_of_monthly_cf(cf_B, m)
    fv_C = future_value_of_monthly_cf(cf_C, m)

    print("\nPart (b): FV at year end if payouts reinvested at 6.5% p.a. (per P=1)")
    # with reinvestment, earlier cash flows have more time to grow, so typically C > B > A
    print("A: {:.8f}".format(fv_A))
    print("B: {:.8f}".format(fv_B))
    print("C: {:.8f}".format(fv_C))

"""
For EAR (capitalizing interest): B is best.

For monthly cash payouts with no reinvestment: all equal.

For monthly payouts with reinvestment at a positive rate: C is best, then B, then A.
"""