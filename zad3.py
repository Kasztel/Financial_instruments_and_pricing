import math

def calculate_nominal_rate_discrete(inflation_rate, n):
    """
    Calculates the nominal interest rate 'r' required to achieve an
    effective annual rate equal to the inflation_rate, compounded 'n'
    times per year.
    
    The formula is derived from:
    (1 + EAR) = (1 + r/n)^n
    
    Solving for r:
    (1 + inflation_rate)^(1/n) = 1 + r/n
    (1 + inflation_rate)^(1/n) - 1 = r/n
    r = n * ((1 + inflation_rate)^(1/n) - 1)
    """
    if n <= 0:
        raise ValueError("Number of compounding periods 'n' must be positive.")
    
    effective_rate_per_period = pow(1 + inflation_rate, 1/n)
    r = n * (effective_rate_per_period - 1)
    return r

def calculate_nominal_rate_continuous(inflation_rate):
    """
    Calculates the nominal interest rate 'r' required to achieve an
    effective annual rate equal to the inflation_rate, with
    continuous compounding.
    
    The formula is derived from:
    (1 + EAR) = e^r
    Where EAR is set to the inflation_rate.
    
    Solving for r:
    ln(1 + inflation_rate) = r
    """
    r = math.log(1 + inflation_rate)
    return r

def main():
    INFLATION_RATE = 0.10 # 10% p.a.
        
    # Compounding periods definition 
    compounding_periods = {
        "Yearly": 1,
        "Half-yearly": 2,
        "Quarterly": 4,
        "Monthly": 12,
        "Daily": 365, # Added purely for comaprison
        "Half-daily": 730 # Same as above
    }
    
    # Discrete compounding
    for name, n in compounding_periods.items():
        rate = calculate_nominal_rate_discrete(INFLATION_RATE, n)
        print(f"For {name:<12} (n={n:<3}) compounding, the required nominal rate r = {rate * 100:.4f}%")
        
    # Continuous compounding
    rate_continuous = calculate_nominal_rate_continuous(INFLATION_RATE)
    print(f"For {'Continuous':<12} (n=inf) compounding, the required nominal rate r = {rate_continuous * 100:.4f}%")

if __name__ == "__main__":
    main()