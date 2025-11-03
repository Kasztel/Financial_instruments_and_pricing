def calculate_simple_interest_payment(fv, years, rate, payments_per_year):
    total_payments_num = years * payments_per_year
    rate_divided = rate / payments_per_year

    n_sum = total_payments_num * (total_payments_num + 1) / 2

    # REASONING:
    #                               |        Q1       |          Q2          |          Q3          |     |              Q(LAST)
    # fv = a * total_payments_num + (a * rate_divided + 2 * a * rate_divided + 3 * a * rate_divided + ... + total_payments_num * a * rate_divided)
    # fv = a * total_payments_num + (1 * rate_divided + 2 * 1 * rate_divided + 3 * 1 * rate_divided + ... + total_payments_num * 1 * rate_divided) * a
    # fv = a * total_payments_num + (rate_divided + 2 * rate_divided + 3 * rate_divided + ... + total_payments_num * rate_divided) * a
    # fv = a * total_payments_num + (1 + 2 + 3 + ... + total_payments_num) * a * rate_divided
    # fv = (total_payments_num + (1 + 2 + 3 + ... + total_payments_num) * rate_divided) * a
    # a = fv / (total_payments_num + (1 + 2 + 3 + ... + total_payments_num) * rate_divided)

    a = fv / (total_payments_num + n_sum * rate_divided)
    return a


def calculate_compound_interest_payment_loop(fv, years, rate, payments_per_year):
    total_payments_num = years * payments_per_year
    rate_divided = rate / payments_per_year

    denominator = 1
    multiplier = rate_divided + 1
    for _ in range(total_payments_num):
        # adding interest for the quarter just ended (denominator * multiplier) and adding quarterly contribution fo beginning quarter (+ 1)
        denominator = denominator * multiplier + 1
    denominator -= 1

    # REASONING:
    #             |      Q1      |        Q2       |        Q3       | ..... |     Q(LAST)   |
    # fv = ( ...(((multiplier * a + a) * multiplier + a) * multiplier + a) ... ) * multiplier

    # fv = ( ...(((multiplier * 1 + 1) * a * multiplier + a) * multiplier + a) ... ) * multiplier
    # fv = ( ...(((multiplier + 1)* 1 * multiplier + 1) * a * multiplier + a) ... ) * multiplier
    # fv = ( ...(((multiplier + 1) * multiplier + 1) * multiplier + 1) ... ) * a * multiplier
    # fv = ( ...(((multiplier + 1) * multiplier + 1) * multiplier + 1) ... ) * multiplier * a
    # a = fv / (( ...(((multiplier + 1) * multiplier + 1) * multiplier + 1) ... ) * multiplier)

    a = fv / denominator
    return a


future_value = 10000
investment_years = 2
savings_annual_rate = 0.05
quarterly_payments_per_year = 4

simple_interest_payment = calculate_simple_interest_payment(
    fv=future_value,
    years=investment_years,
    rate=savings_annual_rate,
    payments_per_year=quarterly_payments_per_year
)

compound_interest_payment = calculate_compound_interest_payment_loop(
    fv=future_value,
    years=investment_years,
    rate=savings_annual_rate,
    payments_per_year=quarterly_payments_per_year
)

print("a) Simple interest:")
print(f"   To accumulate {future_value} PLN AFTER 2 years, the required quarterly payment is: {simple_interest_payment:.2f} PLN")
print()
print("b) Compound interest:")
print(f"   To accumulate {future_value} PLN AFTER 2 years, the required quarterly payment is: {compound_interest_payment:.2f} PLN")