def calculate_bond_metrics(cash_flows, ytm):
    price = 0.0
    mac_dur_sum = 0.0
    conv_sum = 0.0

    for t, cf in cash_flows:
        pv_cf = cf / ((1 + ytm) ** t)
        price += pv_cf
        mac_dur_sum += t * pv_cf
        conv_sum += t * (t + 1) * pv_cf

    macaulay_duration = mac_dur_sum / price
    modified_duration = macaulay_duration / (1 + ytm)

    convexity = (conv_sum / price) / ((1 + ytm) ** 2)

    return price, modified_duration, convexity


def calculate_exact_price_change(cash_flows, old_ytm, new_ytm):
    old_price, _, _ = calculate_bond_metrics(cash_flows, old_ytm)
    new_price, _, _ = calculate_bond_metrics(cash_flows, new_ytm)

    pct_change = (new_price - old_price) / old_price
    return pct_change, old_price, new_price


fv = 1000.0
ytm_initial = 0.0929
shock = 0.05

bond_a_flows = []
coupon_a = 0.04 * fv
maturity_a = 4
for t in range(1, maturity_a + 1):
    cf = coupon_a
    if t == maturity_a:
        cf += fv
    bond_a_flows.append((t, cf))

bond_b_flows = [(3.75, fv)]


print("a)")
price_a, md_a, conv_a = calculate_bond_metrics(bond_a_flows, ytm_initial)
price_b, md_b, conv_b = calculate_bond_metrics(bond_b_flows, ytm_initial)

print(f"BOND A:")
print(f"Price: {price_a:.5f}")
print(f"Modified Duration: {md_a:.5f}")
print(f"Convexity: {conv_a:.5f}")

print(f"\nBOND B:")
print(f"Price: {price_b:.5f}")
print(f"Modified Duration: {md_b:.5f}")
print(f"Convexity: {conv_b:.5f}")




print("\nb)")

scenarios = [
    ("YTM DECREASE (-5%)", ytm_initial - shock),
    ("YTM INCREASE (+5%)", ytm_initial + shock)
]

for label, new_ytm in scenarios:
    print(f"SCENARIO: {label} (New YTM: {new_ytm:.2%})")
    ret_a, old_p_a, new_p_a = calculate_exact_price_change(bond_a_flows, ytm_initial, new_ytm)
    ret_b, old_p_b, new_p_b = calculate_exact_price_change(bond_b_flows, ytm_initial, new_ytm)

    print(f"BOND A: Price change: {ret_a:+.4%} (from {old_p_a:.2f} to {new_p_a:.2f})")
    print(f"BOND B: Price change: {ret_b:+.4%} (from {old_p_b:.2f} to {new_p_b:.2f})")

    if ret_a > ret_b:
        print("Bond A performed better")
    else:
        print("Bond B performed better")
    print()