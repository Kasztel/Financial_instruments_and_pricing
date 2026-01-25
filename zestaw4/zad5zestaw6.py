import numpy as np
import scipy.stats as si

# Parametry zadania
S0 = 1.0     # Cena początkowa
X = 1.0      # Cena wykonania
T = 1.0      # Czas do wygaśnięcia (1 rok)
sigma = 0.2  # Zmienność (20%)
r = 0.1      # Stopa wolna od ryzyka (10%) - ciągła
np.random.seed(42) 

# Funkcja analityczna Blacka-Scholesa (dla porównania)
def bs_price(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * si.norm.cdf(d1) - X * np.exp(-r * T) * si.norm.cdf(d2)
    elif option_type == 'binary':
        # Dla opcji binarnej call: e^(-rT) * N(d2)
        price = np.exp(-r * T) * si.norm.cdf(d2)
    return price

# a. Wycena Europejskiej Opcji Kupna (MC vs BS) 
print("a. Wycena Europejskiej Opcji Call (Monte Carlo)")
bs_call = bs_price(S0, X, T, r, sigma, 'call')
print(f"Analityczna cena Blacka-Scholesa: {bs_call:.6f}")

simulations = [1000, 10000, 100000] # Liczba trajektorii

for M in simulations:
    # 1. Generowanie zmiennych losowych z rozkładu normalnego N(0,1)
    Z = np.random.standard_normal(M)
    
    # 2. Symulacja ceny końcowej S(T)
    # Wzór: S_T = S0 * exp((r - 0.5 * sigma^2)*T + sigma * sqrt(T) * Z)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # 3. Obliczenie wypłaty (Payoff) = max(S(T) - X, 0)
    payoffs = np.maximum(ST - X, 0)
    
    # 4. Dyskontowanie średniej wypłaty e^(-rT)
    mc_price = np.exp(-r * T) * np.mean(payoffs)
    
    # 5. Błąd statystyczny
    # SE = std(payoffs) / sqrt(M)
    # Należy pamiętać o zdyskontowaniu odchylenia standardowego lub wyniku końcowego
    std_error = (np.std(payoffs) * np.exp(-r * T)) / np.sqrt(M)
    
    print(f"Symulacje: {M:6d} | Cena MC: {mc_price:.6f} | Blad (+/-): {std_error:.6f} | Roznica vs BS: {mc_price - bs_call:.6f}")

# b. Wycena Europejskiej Opcji Binarnej
print("b. Wycena Europejskiej Opcji Binarnej Call")
# Payoff: 1 jeśli S(T) > X, w przeciwnym razie 0

bs_binary = bs_price(S0, X, T, r, sigma, 'binary')
print(f"Analityczna cena Binary (BS): {bs_binary:.6f}")

M = 100000 # Używamy największej próby dla dokładności
Z = np.random.standard_normal(M)
ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

# Payoff binarny: Heaviside step function
binary_payoffs = np.where(ST > X, 1.0, 0.0)

mc_binary_price = np.exp(-r * T) * np.mean(binary_payoffs)
std_error_bin = (np.std(binary_payoffs) * np.exp(-r * T)) / np.sqrt(M)

print(f"Symulacje: {M} | Cena MC: {mc_binary_price:.6f} | Blad: {std_error_bin:.6f}")


# c. Opcja sinusoidalna ("Strange sinusoidal") 
print("c. Wycena Opcji Sinusoidalnej")
# Payoff: sin(S(T)) dla S(T) <= pi, 0 dla S(T) > pi

# Używamy tych samych ST co wyżej (M=100k)
sin_payoffs = np.where(ST <= np.pi, np.sin(ST), 0.0)

mc_sin_price = np.exp(-r * T) * np.mean(sin_payoffs)
std_error_sin = (np.std(sin_payoffs) * np.exp(-r * T)) / np.sqrt(M)

print(f"Symulacje: {M} | Cena MC: {mc_sin_price:.6f} | Blad: {std_error_sin:.6f}")

# d. Asian Call Option (Path dependent) 
print("d. Wycena Opcji Azjatyckiej (Asian Call)")
# Payoff: max(Average(S) - X, 0)
# Wymaga generowania całej ścieżki, nie tylko punktu końcowego.

dt = 1.0 / 250.0  # Krok czasowy (np. dni handlowe)
steps = int(T / dt) # Liczba kroków (250)
M_asian = 10000     # Liczba ścieżek (zmniejszona nieco ze względu na złożoność obliczeniową)

print(f"Generowanie {M_asian} sciezek po {steps} krokow czasowych (dt={dt})...")

# Inicjalizacja macierzy cen: [M_asian, steps + 1]
# Zaczynamy od S0
S_paths = np.zeros((M_asian, steps + 1))
S_paths[:, 0] = S0

# Generowanie ścieżek (Brownian Motion)
# S(t+dt) = S(t) * exp((r - 0.5*sigma^2)dt + sigma*sqrt(dt)*Z)
drift = (r - 0.5 * sigma**2) * dt
vol = sigma * np.sqrt(dt)

for t in range(1, steps + 1):
    Z_t = np.random.standard_normal(M_asian)
    S_paths[:, t] = S_paths[:, t-1] * np.exp(drift + vol * Z_t)

# Obliczenie średniej arytmetycznej dla każdej ścieżki
# Axis 1 to czas
average_prices = np.mean(S_paths, axis=1)

# Payoff opcji azjatyckiej
asian_payoffs = np.maximum(average_prices - X, 0)

mc_asian_price = np.exp(-r * T) * np.mean(asian_payoffs)
std_error_asian = (np.std(asian_payoffs) * np.exp(-r * T)) / np.sqrt(M_asian)

print(f"Cena MC Opcji Azjatyckiej: {mc_asian_price:.6f} | Blad: {std_error_asian:.6f}")