import math

def print_schedule(name, schedule, total_interest):
    """
    Helper function for printing schedules
    """
    print(f"\n--- Amortization Schedule: {name} ---")
    print("=" * 80)
    print(f"{'Period':<8} | {'Initial Principal':<18} | {'Total Payment (CF)':<18} | {'Interest Payment':<18} | {'Principal Payment':<18}")
    print("-" * 80)
    
    for row in schedule:
        print(f"{row['period']:<8} | {row['initial_principal']:<18,.2f} | {row['total_payment']:<18,.2f} | {row['interest_payment']:<18,.2f} | {row['principal_payment']:<18,.2f}")
    
    print("=" * 80)
    print(f"Total Interest Paid: {total_interest:,.2f} PLN\n")

def calculate_constant_principal_schedule(P, r_pa, T_years, n_per_year):
    """
    Calculates the amortization schedule for equal principal payments.
    
    The principal payment is constant, and interest is paid on the outstanding balance.
    """
    schedule = []
    total_interest = 0
    
    r_p = r_pa / n_per_year  # Periodic interest rate (per quarter)
    N = T_years * n_per_year # Total number of periods
    
    principal_payment = P / N # Constant principal payment
    current_principal = P
    
    for k in range(1, N + 1):
        interest_payment = current_principal * r_p
        total_payment = principal_payment + interest_payment
        
        schedule.append({
            'period': k,
            'initial_principal': current_principal,
            'total_payment': total_payment,
            'interest_payment': interest_payment,
            'principal_payment': principal_payment
        })
        
        total_interest += interest_payment
        current_principal -= principal_payment
        
    return schedule, total_interest

def calculate_annuity_schedule(P, r_pa, T_years, n_per_year):
    """
    Calculates the amortization schedule for equal total payments.
    
    We first find the constant payment PMT using the PVA formula.
    """
    schedule = []
    total_interest = 0
    
    r_p = r_pa / n_per_year  # Periodic interest rate (per quarter)
    N = T_years * n_per_year # Total number of periods
    
    # Calculate the constant periodic payment (PMT) using the
    # Present Value of an Annuity (PVA) formula: P = PMT * [ (1 - (1+r_p)^-N) / r_p ]
    # Solved for PMT:
    if r_p > 0:
        total_payment = P * (r_p / (1 - math.pow(1 + r_p, -N)))
    else:
        total_payment = P / N # Handle zero interest case
        
    current_principal = P
    
    for k in range(1, N + 1):
        interest_payment = current_principal * r_p
        principal_payment = total_payment - interest_payment
        
        schedule.append({
            'period': k,
            'initial_principal': current_principal,
            'total_payment': total_payment,
            'interest_payment': interest_payment,
            'principal_payment': principal_payment
        })
        
        total_interest += interest_payment
        current_principal -= principal_payment
        
    return schedule, total_interest

def calculate_effective_rate(r_pa, n_per_year):
    """
    Calculates the Effective Annual Rate (y) from the Nominal Rate (r)
    and compounding frequency (n).

    Formula: y = (1 + r/n)^n - 1
    """
    y = math.pow(1 + r_pa / n_per_year, n_per_year) - 1
    return y

def main():
    # --- Constants ---
    P_LOAN = 10000.0   # Initial Principal (PLN)
    R_NOMINAL = 0.10   # (10% p.a.)
    T_YEARS = 1        # Loan term in years
    N_PER_YEAR = 4     # Compounding frequency (quarterly)
    
    # Equal Principal Payments
    schedule1, interest1 = calculate_constant_principal_schedule(P_LOAN, R_NOMINAL, T_YEARS, N_PER_YEAR)
    print_schedule("Equal Principal Payments", schedule1, interest1)
    
    # Equal Total Payments (Annuity)
    schedule2, interest2 = calculate_annuity_schedule(P_LOAN, R_NOMINAL, T_YEARS, N_PER_YEAR)
    print_schedule("Equal Total Payments (Annuity)", schedule2, interest2)

    # Compute Effective Interest Rate (EIR) and Analysis 
    print("\nAnalysis: EIR and Favourability")
    print("=" * 80)
    
    # Calculate Effective Interest Rate (y)
    eir_y = calculate_effective_rate(R_NOMINAL, N_PER_YEAR)
    print(f"1. Effective Interest Rate (EIR / y):")
    print(f"   y = (1 + r/n)^n - 1 = (1 + {R_NOMINAL}/{N_PER_YEAR})^{N_PER_YEAR} - 1 = {eir_y * 100:.4f}%")
    
    print(f"\n2. Favourability:")
    print(f"   For the Client: Scheme 1 (Equal Principal) is more favourable.")
    print(f"   Why? The client pays less total interest ({interest1:,.2f} PLN) because")
    print("   they pay back principal faster, reducing the outstanding balance sooner.")
    
    print(f"\n   For the Bank: Scheme 2 (Annuity) is more favourable.")
    print(f"   Why? The bank earns more total interest ({interest2:,.2f} PLN) because")
    print("   the principal balance remains higher for longer.")
    print("=" * 80)

if __name__ == "__main__":
    main()