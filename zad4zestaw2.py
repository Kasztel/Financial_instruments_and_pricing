face_value = 1000
coupon_rate = 0.05
ytm_initial = 0.06
maturity_years = 2.5

times = [0.5, 1.5, 2.5]

coupon_payment = face_value * coupon_rate
cash_flows = [coupon_payment, coupon_payment, coupon_payment + face_value]

price_initial = sum([cf / ((1 + ytm_initial) ** t) for cf, t in zip(cash_flows, times)])

weighted_pv_sum = sum([(t * cf) / ((1 + ytm_initial) ** t) for cf, t in zip(cash_flows, times)])
mac_duration = weighted_pv_sum / price_initial

mod_duration = mac_duration / (1 + ytm_initial)

print(f"INITIAL BOND:")
print(f"Face Value: {face_value} PLN")
print(f"Current YTM: {ytm_initial * 100:.2f}%")
print(f"Dirty Price (P): {price_initial:.4f} PLN")
print(f"Macaulay Dur.: {mac_duration:.4f} years")
print(f"Modified Dur.: {mod_duration:.4f} years")

scenarios = {
    'a)': 0.001,
    'b)': -0.001,
    'c)': 0.005,
    'd)': -0.005
}

results = []

for label, d_ytm in scenarios.items():
    ytm_new = ytm_initial + d_ytm
    price_new = sum([cf / ((1 + ytm_new) ** t) for cf, t in zip(cash_flows, times)])
    change_exact = price_new - price_initial
    change_approx = -mod_duration * price_initial * d_ytm

    results.append({
        "Scenario": label,
        "YTM": f"{ytm_new * 100:.2f}%",
        "Exact dP": change_exact,
        "Approx dP": change_approx,
    })

print("\nRESULTS:")
print(f"{'Scen.':<6} | {'YTM':<8} | {'Exact dP (PLN)':<15} | {'Approx dP (PLN)':<15}")
print("-"*53)
for row in results:
    print(f"{row['Scenario']:<6} | {row['YTM']:<8} | {row['Exact dP']:<15.5f} | {row['Approx dP']:<15.5f}")
