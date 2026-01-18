from datetime import date


def calculate_fra_settlement():
    notional = 10000000
    fra_rate = 0.0456
    floating_rate = 0.0419
    value_date = date(2025, 12, 3)
    maturity_date = date(2026, 3, 3)
    basis = 365

    days_count = (maturity_date - value_date).days
    time_factor = days_count / basis
    interest_diff = (floating_rate - fra_rate) * notional * time_factor
    discount_factor = 1 + (floating_rate * time_factor)
    net_cash_flow = interest_diff / discount_factor

    print(f"Number of days (d): {days_count}")
    print(f"Net Cash Flow (CF): {net_cash_flow:,.2f} PLN\n")

    print(f"1. When will the payment be done? \nAnswer: On the value date, which is {value_date}.")

    who_pays = "the party paying the fixed interest rate" if net_cash_flow < 0 else "the party receiving the fixed interest rate"

    print(f"\n2. Who will pay net CF? \nAnswer: {who_pays}.")


if __name__ == "__main__":
    calculate_fra_settlement()