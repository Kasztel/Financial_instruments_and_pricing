import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb


def get_binomial_price(S, X, u, d, R, N, kind):
    if u <= 1 + R or 1 + R <= d:
        return np.nan

    g = ((1 + R) - d) / (u - d)

    price = 0.0
    for j in range(N + 1):
        S_final = S * (u ** j) * (d ** (N - j))

        if kind == 'binary':
            payoff = 1.0 if S_final > X else 0.0
        elif kind == 'call':
            payoff = max(S_final - X, 0.0)
        elif kind == 'put':
            payoff = max(X - S_final, 0.0)
        else:
            payoff = 0.0

        prob = comb(N, j) * (g ** j) * ((1 - g) ** (N - j))
        price += prob * payoff

    return price * ((1 + R) ** -N)


S0 = 1.0
X0 = 1.0
u0 = 1.05
d0 = 1.0 / u0
R0 = 0.025
N0 = 11

p_binary = get_binomial_price(S0, X0, u0, d0, R0, N0, 'binary')
p_call = get_binomial_price(S0, X0, u0, d0, R0, N0, 'call')
p_put = get_binomial_price(S0, X0, u0, d0, R0, N0, 'put')

print(f"Binary Option Price: {p_binary:.6f}")
print(f"Call Option Price: {p_call:.6f}")
print(f"Put Option Price: {p_put:.6f}")

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

s_vals = np.linspace(0.8, 1.2, 50)
prices_s = [[get_binomial_price(s, X0, u0, d0, R0, N0, k) for k in ['call', 'put', 'binary']] for s in s_vals]
prices_s = np.array(prices_s)
axs[0, 0].plot(s_vals, prices_s[:, 0], label='Call')
axs[0, 0].plot(s_vals, prices_s[:, 1], label='Put')
axs[0, 0].plot(s_vals, prices_s[:, 2], label='Binary')
axs[0, 0].set_xlabel('Spot Price S')
axs[0, 0].set_ylabel('Option Price')
axs[0, 0].legend()
axs[0, 0].set_title('Price vs S')

x_vals = np.linspace(0.8, 1.2, 50)
prices_x = [[get_binomial_price(S0, x, u0, d0, R0, N0, k) for k in ['call', 'put', 'binary']] for x in x_vals]
prices_x = np.array(prices_x)
axs[0, 1].plot(x_vals, prices_x[:, 0], label='Call')
axs[0, 1].plot(x_vals, prices_x[:, 1], label='Put')
axs[0, 1].plot(x_vals, prices_x[:, 2], label='Binary')
axs[0, 1].set_xlabel('Exercise Price X')
axs[0, 1].set_ylabel('Option Price')
axs[0, 1].legend()
axs[0, 1].set_title('Price vs X')

r_vals = np.linspace(0.0, 0.04, 50)
prices_r = [[get_binomial_price(S0, X0, u0, d0, r, N0, k) for k in ['call', 'put', 'binary']] for r in r_vals]
prices_r = np.array(prices_r)
axs[1, 0].plot(r_vals, prices_r[:, 0], label='Call')
axs[1, 0].plot(r_vals, prices_r[:, 1], label='Put')
axs[1, 0].plot(r_vals, prices_r[:, 2], label='Binary')
axs[1, 0].set_xlabel('Interest Rate R')
axs[1, 0].set_ylabel('Option Price')
axs[1, 0].legend()
axs[1, 0].set_title('Price vs R')

u_vals = np.linspace(1.00, 1.1, 50)
prices_u = []
valid_u = []
for u_ in u_vals:
    d_ = 1.0 / u_
    if d_ < 1 + R0 < u_:
        prices_u.append([get_binomial_price(S0, X0, u_, d_, R0, N0, k) for k in ['call', 'put', 'binary']])
        valid_u.append(u_)
prices_u = np.array(prices_u)
axs[1, 1].plot(valid_u, prices_u[:, 0], label='Call')
axs[1, 1].plot(valid_u, prices_u[:, 1], label='Put')
axs[1, 1].plot(valid_u, prices_u[:, 2], label='Binary')
axs[1, 1].set_xlabel('Up Factor u')
axs[1, 1].set_ylabel('Option Price')
axs[1, 1].legend()
axs[1, 1].set_title('Price vs u')

plt.tight_layout()
plt.savefig('zad2_plots.png')