import math

def calculate_equivalent_periodic_rate(annual_effective_rate, n):
    """
    Calculates the equivalent effective periodic (quarterly, monthly...) rate
    that corresponds to a given annual effective rate 'y'.

    The formula is derived from:
    (1 + y_periodic)^n = (1 + y_annual)
    
    Solving for y_periodic:
    y_periodic = (1 + y_annual)^(1/n) - 1
    """
    if n <= 0:
        raise ValueError("Number of compounding periods 'n' must be positive.")
    
    y_periodic = pow(1 + annual_effective_rate, 1/n) - 1
    return y_periodic

def calculate_equivalent_continuous_rate(annual_effective_rate):
    """
    Calculates the equivalent effective continuous rate 'r' for a
    given annual effective rate 'y'.
    
    The formula is derived from:
    exp(r) = (1 + y)
    
    Solving for r:
    r = ln(1 + y)
    """
    r = math.log(1 + annual_effective_rate)
    return r

def main():
    Y_ANNUAL = 0.05 # 5% p.a.
    
    print(f"Given Annual Effective Rate (y) = {Y_ANNUAL * 100:.1f}%\n")
    
    print("--- Part (a): Equivalent Effective Periodic Rates ---")
    
    periodic_calcs = {
        "Quarterly": 4,
        "Monthly": 12,
        "Weekly": 52,
        "Daily": 365
    }
        
    for name, n in periodic_calcs.items():
        y_p = calculate_equivalent_periodic_rate(Y_ANNUAL, n)
        print(f"Equivalent {name:<10} rate (y_p): {y_p * 100:.6f}%")
    
    print("\n--- Part (b): Equivalent Effective Continuous Rate ---")
        
    r = calculate_equivalent_continuous_rate(Y_ANNUAL)
    print(f"Equivalent Continuous Rate (r): {r * 100:.6f}%")

if __name__ == "__main__":
    main()