import pandas as pd

# Data (in billions PLN)
A_loans = 1.0
MD_loans = 1.0

A_bonds = 1.0
MD_bonds = 3.0

A_total = A_loans + A_bonds

L_deposits = 2.0
MD_deposits = 1.5  # liability modified duration

# Switch trade: sell x of 10Y bonds (MD=10) and buy x of 1Y bonds (MD=1)
MD_10y = 10.0
MD_1y  = 1.0

# Current asset MD (value-weighted)
MD_assets_current = (A_loans * MD_loans + A_bonds * MD_bonds) / A_total

# Immunization target (here A_total == L_deposits, so match MDs)
MD_assets_target = MD_deposits

# Required MD of the bond portfolio after the switch
# MD_assets_target = (A_loans*MD_loans + A_bonds*MD_bonds_new) / A_total
MD_bonds_required = (MD_assets_target * A_total - A_loans * MD_loans) / A_bonds

# Bond-portfolio MD after the switch:
# MD_bonds_new = MD_bonds + (MD_1y - MD_10y) * (x / A_bonds)
# Solve for x:
x = (MD_bonds_required - MD_bonds) / (MD_1y - MD_10y) * A_bonds  # in billions PLN

result = pd.DataFrame([{
    "MD_assets_current": MD_assets_current,
    "MD_assets_target": MD_assets_target,
    "MD_bonds_required": MD_bonds_required,
    "x_to_sell_10y_(bln_PLN)": x,
    "x_to_sell_10y_(mln_PLN)": x * 1000
}])

print(result.to_string(index=False))

'''
Conclusion:

The bank initially has a positive duration gap (𝑀𝐷_𝐴 = 2.0 vs. 𝑀𝐷_𝐿 = 1.5), so its equity value would fall when interest rates rise.

To immunize (for small parallel yield changes), the bank should reduce asset interest-rate sensitivity until 𝑀𝐷_𝐴 ≈ 𝑀𝐷_𝐿.

Since loans are unchanged, the bond portfolio duration must drop from 3.0 to 2.0, achieved by selling ~111.11 mln PLN of 10-year bonds and replacing them with 1-year bonds.

After the switch, the balance sheet becomes less exposed to interest-rate risk (smaller price impact from yield shifts).
'''