import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def solve_yield_curve():
    # Bond Data
    # 'Price' is the Dirty Price (Clean Price + Accrued Interest) provided in the table
    data = [
        {'Name': 'AAA', 'Maturity': 0.5, 'Coupon': 0.04, 'Price': 101.98},
        {'Name': 'BBB', 'Maturity': 1.0, 'Coupon': 0.04, 'Price': 99.57},
        {'Name': 'CCC', 'Maturity': 1.5, 'Coupon': 0.03, 'Price': 98.88},
        {'Name': 'DDD', 'Maturity': 2.0, 'Coupon': 0.04, 'Price': 97.80},
        {'Name': 'EEE', 'Maturity': 2.5, 'Coupon': 0.04, 'Price': 98.62},
        {'Name': 'FFF', 'Maturity': 3.0, 'Coupon': 0.00, 'Price': 84.56},
        {'Name': 'GGG', 'Maturity': 3.5, 'Coupon': 0.05, 'Price': 99.70},
        {'Name': 'HHH', 'Maturity': 4.0, 'Coupon': 0.00, 'Price': 78.91},
        {'Name': 'JJJ', 'Maturity': 4.5, 'Coupon': 0.00, 'Price': 76.29},
        {'Name': 'KKK', 'Maturity': 5.0, 'Coupon': 0.04, 'Price': 90.79}
    ]

    df = pd.DataFrame(data)

    # Dictionary to store Discount Factors Z(t)
    # Z(t) = 1 / (1 + r)^t
    discount_factors = {}

    results = []

    print(f"{'Bond':<5} {'Maturity':<10} {'Price':<10} {'Calc Zero Rate %':<15}")
    print("-" * 45)

    # Bootstrapping Loop
    for index, row in df.iterrows():
        mat = row['Maturity']
        coupon_rate = row['Coupon']
        dirty_price = row['Price']
        face_value = 100

        # Determine Cash Flow times
        # "Coupons paid annually, last on maturity"
        # If maturity is 1.5, flows are at 0.5 and 1.5
        # If maturity is 2.0, flows are at 1.0 and 2.0
        if mat % 1 == 0:
            cf_times = np.arange(1.0, mat + 0.1, 1.0)
        else:
            cf_times = np.arange(0.5, mat + 0.1, 1.0)

        # Calculate PV of coupons prior to maturity
        pv_coupons = 0
        final_time = cf_times[-1]  # This is equal to mat

        # We process times excluding the final maturity first to subtract their PV
        for t in cf_times[:-1]:
            if t in discount_factors:
                coupon_payment = coupon_rate * face_value
                pv_coupons += coupon_payment * discount_factors[t]
            else:
                raise ValueError(f"Missing discount factor for time {t}. Data must be sorted by maturity.")

        # Solve for the Discount Factor at Maturity (Df_T)
        # Price = PV_prior_coupons + (Face + Coupon) * Df_T
        # Df_T = (Price - PV_prior_coupons) / (Face + Coupon)

        final_cash_flow = face_value + (coupon_rate * face_value)
        df_maturity = (dirty_price - pv_coupons) / final_cash_flow

        # Store discount factor
        discount_factors[final_time] = df_maturity

        # Calculate Zero Rate (Annual Compounding)
        # Z(t) = 1 / (1 + r)^t  =>  r = (1 / Z(t))^(1/t) - 1
        zero_rate = (1.0 / df_maturity) ** (1.0 / final_time) - 1.0

        results.append((final_time, zero_rate))
        print(f"{row['Name']:<5} {mat:<10} {dirty_price:<10} {zero_rate * 100:.4f}%")

    # Fitting quadratic function y(t) = at^2 + bt + c
    t_values = np.array([r[0] for r in results])
    y_values = np.array([r[1] for r in results])  # Zero rates

    coeffs = np.polyfit(t_values, y_values, 2)
    a, b, c = coeffs

    print("-" * 45)
    print("\nFitted Quadratic Function Parameters:")
    print(f"y(t) = a*t^2 + b*t + c")
    print(f"a = {a:.6f}")
    print(f"b = {b:.6f}")
    print(f"c = {c:.6f}")

    # Optional: Generate points for plotting
    t_smooth = np.linspace(t_values.min(), t_values.max(), 100)
    y_smooth = a * t_smooth ** 2 + b * t_smooth + c

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(t_values, y_values, color='red', label='Bootstrapped Rates')
    plt.plot(t_smooth, y_smooth, label=f'Fit: {a:.5f}$t^2$ + {b:.5f}t + {c:.5f}')
    plt.xlabel('Time to Maturity (Years)')
    plt.ylabel('Zero Rate')
    plt.title('Zero Coupon Yield Curve')
    plt.legend()
    plt.grid(True)
    plt.savefig("figure_01")


if __name__ == "__main__":
    solve_yield_curve()
