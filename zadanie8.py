loan_amount = 500_000          # loan principal (PLN)
years = 30                     # loan term in years
months = years * 12            # total number of monthly installments (30 * 12 = 360)

# e) monthly payment for the first 3 months
# Interest rate: WIBOR3M 4.5% + margin 1% = 5.5% p.a.
annual_rate_initial = 0.045 + 0.01          # 5.5% = 0.055
monthly_rate_initial = annual_rate_initial / 12   # convert annual rate to monthly rate

# Annuity (equal) payment formula:
# A = P * r / (1 - (1 + r)^(-n))
# where:
# P - loan principal
# r - monthly interest rate
# n - number of payments
P = loan_amount
r = monthly_rate_initial
n = months

monthly_payment_initial = P * r / (1 - (1 + r) ** (-n))

print("e) Monthly payment (first 3 months):", round(monthly_payment_initial, 2), "PLN")

# f) outstanding balance after 3 months
# Outstanding balance after k payments for an annuity loan:
# B_k = P * (1 + r)^k - A * ((1 + r)^k - 1) / r
# where:
# B_k - balance after k months
# k   - number of paid installments
k = 3
balance_after_3m = P * (1 + r) ** k - monthly_payment_initial * (((1 + r) ** k - 1) / r)

print("f) Outstanding balance after 3 months:", round(balance_after_3m, 2), "PLN")

# g) new monthly payment for the next 3 months (after rate change)
# After 3 months WIBOR3M drops to 4%, so new annual rate = 4% + 1% = 5% p.a.
annual_rate_new = 0.04 + 0.01     # 5% = 0.05
monthly_rate_new = annual_rate_new / 12

# Remaining term: 360 - 3 = 357 months
remaining_months = months - k

# We now recalculate the annuity payment using:
# A_new = B * r_new / (1 - (1 + r_new)^(-n_remaining))
# where:
# B - outstanding balance after 3 months
# r_new - new monthly interest rate
# n_remaining - remaining number of installments
B = balance_after_3m
r_new = monthly_rate_new
n_remaining = remaining_months

monthly_payment_new = B * r_new / (1 - (1 + r_new) ** (-n_remaining))

print("g) New monthly payment (months 4-6):", round(monthly_payment_new, 2), "PLN")
