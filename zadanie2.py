"""
Doubling time under different compounding conventions.
Formulas derived for A/P = 2 with nominal annual rate r (R = r_decimal).
"""
import math

def t_simple(R: float) -> float:
    """Simple interest: A = P(1 + R t) -> t = 1/R"""
    if R <= 0:
        raise ValueError("R must be positive")
    return 1.0 / R

def t_compound(R: float, n: float) -> float:
    """Compound interest n times per year: A = P(1 + R/n)^(n t) -> t = ln 2 / (n ln(1 + R/n))"""
    if R <= 0 or n <= 0:
        raise ValueError("R and n must be positive.")
    return math.log(2.0) / (n * math.log(1.0 + R / n))

def t_continuous(R: float) -> float:
    """Continuous compounding: A = P e^{Rt} -> t = ln 2 / R"""
    if R <= 0:
        raise ValueError("R must be positive.")
    return math.log(2.0) / R

if __name__ == "__main__":
    R = 0.05  # 5%
    print("r = 5% (R=0.05)")
    print(f"(a) Simple interest: t = {t_simple(R):.6f} years")
    for n in [1, 4, 12, 365]:
        print(f"(b) Compound n={n}/year: t = {t_compound(R, n):.6f} years")
    print(f"(c) Continuous compounding: t = {t_continuous(R):.6f} years")
