def calculate_monthly_interest(start_balance, transactions, days_in_month, annual_rate):

    daily_rate = annual_rate / 365
    total_interest = 0.0
    current_balance = start_balance

    processed_through_day = 0
    sorted_transactions = dict(sorted(transactions.items()))
    sorted_transactions[days_in_month + 1] = 0.0

    for day, amount in sorted_transactions.items():
        num_days = (day - 1) - processed_through_day

        if num_days > 0:
            interest_for_period = current_balance * daily_rate * num_days
            total_interest += interest_for_period

        current_balance += amount
        processed_through_day = day - 1


    closing_balance = current_balance + total_interest
    return total_interest, closing_balance


initial_balance_oct = 100000.0
annual_rate = 0.05

# OCTOBER
transactions_oct = {
    5: 17000.0,
    12: 35000.0,
    21: -55000.0
}
interest_oct, closing_balance_oct = calculate_monthly_interest(
    start_balance=initial_balance_oct,
    transactions=transactions_oct,
    days_in_month=31,
    annual_rate=annual_rate
)

# NOVEMBER
transactions_nov = {
    9: -25000.0,
    30: 100000.0
}
interest_nov, closing_balance_nov = calculate_monthly_interest(
    start_balance=closing_balance_oct,  # Saldo początkowe to saldo końcowe z października
    transactions=transactions_nov,
    days_in_month=30,
    annual_rate=annual_rate
)
print("OCTOBER:")
print(f"Interest added to account in October: {interest_oct:.2f} PLN")
print(f"Balance at the end of October: {closing_balance_oct:.2f} PLN")
print()
print("NOVEMBER:")
print(f"Interest added to account in November: {interest_nov:.2f} PLN")
print(f"Balance at the end of November: {closing_balance_nov:.2f} PLN")
