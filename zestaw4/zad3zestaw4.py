import numpy as np
from scipy.special import comb


def get_binomial_forward_price(S, X, u, d, R, N):
    if u <= 1 + R or 1 + R <= d:
        return np.nan

    g = ((1 + R) - d) / (u - d)

    expected_payoff = 0.0
    for j in range(N + 1):
        S_final = S * (u ** j) * (d ** (N - j))
        payoff = S_final - X
        prob = comb(N, j) * (g ** j) * ((1 - g) ** (N - j))
        expected_payoff += prob * payoff

    return expected_payoff * ((1 + R) ** -N)


S = 100.0
X = 90.0
u = 1.1
d = 1.0 / u
R = 0.05
N = 5

model_price = get_binomial_forward_price(S, X, u, d, R, N)
theoretical_price = S - X * ((1 + R) ** -N)

print(f"Parameters: S={S}, X={X}, R={R}, N={N}, u={u}")
print(f"Model Price: {model_price:.10f}")
print(f"Theoretical Price: {theoretical_price:.10f}")
print(f"Difference: {abs(model_price - theoretical_price):.10e}")

if abs(model_price - theoretical_price) < 1e-9:
    print("The Binomial model correctly prices the Forward contract.")
else:
    print("Discrepancy found.")