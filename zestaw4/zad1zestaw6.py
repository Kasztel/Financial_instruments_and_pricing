import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt

# Parametry wejściowe
S = 1.0      # Cena początkowa akcji
u = 1.2      # Czynnik wzrostu
d = 1.0 / u  # Czynnik spadku (d = 1/u)
R = 0.1      # Stopa procentowa za okres (10%)
X = 1.0      # Cena wykonania
N = 3        # Liczba kroków

# Prawdopodobieństwo neutralne względem ryzyka
# Wzór: q = ((1 + R) - d) / (u - d)
q = ((1 + R) - d) / (u - d)

print(f"Parametry modelu:")
print(f"S={S}, X={X}, R={R}, N={N}")
print(f"u={u:.4f}, d={d:.4f}")
print(f"Prawdopodobienstwo neutralne (q) = {q:.4f}")

# Funkcja pomocnicza do budowy drzewa dwumianowego
def binomial_tree_pricing(option_type='call', style='european'):
    """
    Oblicza cenę opcji, drzewo cen, Delta i B.
    option_type: 'call' lub 'put'
    style: 'european' lub 'american'
    """
    
    # 1. Inicjalizacja drzewa cen akcji
    # stock_tree[i][j] to cena w kroku i, węźle j
    stock_tree = [[0.0 for _ in range(i + 1)] for i in range(N + 1)]
    for i in range(N + 1):
        for j in range(i + 1):
            # S_ij = S * u^j * d^(i-j)
            stock_tree[i][j] = S * (u ** j) * (d ** (i - j))

    # 2. Inicjalizacja drzewa wartości opcji (Option Value Tree)
    option_tree = [[0.0 for _ in range(i + 1)] for i in range(N + 1)]
    
    # Obliczenie wypłaty w terminie wygaśnięcia (krok N)
    for j in range(N + 1):
        if option_type == 'call':
            option_tree[N][j] = max(stock_tree[N][j] - X, 0)
        else: # put
            option_tree[N][j] = max(X - stock_tree[N][j], 0)

    # 3. Indukcja wsteczna
    # Przechowujemy też drzewa Delta i B
    delta_tree = [[0.0 for _ in range(i + 1)] for i in range(N)]
    B_tree = [[0.0 for _ in range(i + 1)] for i in range(N)]

    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            # Wartość kontynuacji (zdyskontowana wartość oczekiwana)
            # f = (q * f_up + (1-q) * f_down) / (1 + R)
            f_up = option_tree[i+1][j+1]
            f_down = option_tree[i+1][j]
            continuation_value = (q * f_up + (1 - q) * f_down) / (1 + R)
            
            # Wartość wewnętrzna (tylko dla opcji amerykańskich)
            intrinsic_value = 0
            if option_type == 'call':
                intrinsic_value = max(stock_tree[i][j] - X, 0)
            else:
                intrinsic_value = max(X - stock_tree[i][j], 0)
            
            # Ustalenie ceny opcji w węźle
            if style == 'american':
                option_tree[i][j] = max(intrinsic_value, continuation_value)
            else: # european
                option_tree[i][j] = continuation_value
                
            # Obliczenie Delta i B (Replicating Portfolio)
            # Delta = (f_up - f_down) / (S_up - S_down)
            S_up = stock_tree[i+1][j+1]
            S_down = stock_tree[i+1][j]
            
            delta_val = (f_up - f_down) / (S_up - S_down)
            
            # B = (f_down * u - f_up * d) / ((u - d) * (1 + R))
            # Jest to kwota na koncie bankowym
            B_val = (f_down * u - f_up * d) / ((u - d) * (1 + R))
            
            delta_tree[i][j] = delta_val
            B_tree[i][j] = B_val

    return stock_tree, option_tree, delta_tree, B_tree

# a. American Call Option 
st_ac, opt_ac, delta_ac, b_ac = binomial_tree_pricing('call', 'american')
print( "a. Opcja AMERYKANSKA KUPNA")
print(f"Cena opcji w t=0: {opt_ac[0][0]:.4f}")
print("Drzewo cen opcji (od t=0 do t=3):")
for layer in opt_ac: print([round(x, 4) for x in layer])
print("Drzewo Delta (t=0 do t=2):")
for layer in delta_ac: print([round(x, 4) for x in layer])

# b. European Put Option 
st_ep, opt_ep, delta_ep, b_ep = binomial_tree_pricing('put', 'european')
print(" b. Opcja EUROPEJSKA SPRZEDAZY")
print(f"Cena opcji w t=0: {opt_ep[0][0]:.4f}")
print("Drzewo cen opcji:")
for layer in opt_ep: print([round(x, 4) for x in layer])

# c. American Put Option 
st_ap, opt_ap, delta_ap, b_ap = binomial_tree_pricing('put', 'american')
print("c. Opcja AMERYKANSKA SPRZEDAZY")
print(f"Cena opcji w t=0: {opt_ap[0][0]:.4f}")
print("Drzewo cen opcji:")
for layer in opt_ap: print([round(x, 4) for x in layer])

# d. Sprawdzenie parytetu
print("d. Weryfikacja parytetu")

# Musimy obliczyć cenę Europejskiego Call, żeby sprawdzić pierwszy wzór
_, opt_ec, _, _ = binomial_tree_pricing('call', 'european')

c = opt_ec[0][0]  # European Call
p = opt_ep[0][0]  # European Put
C_amer = opt_ac[0][0] # American Call
P_amer = opt_ap[0][0] # American Put
PV_X = X * ((1 + R)**(-N)) # Zdyskontowana cena wykonania

# 1. Parytet dla opcji europejskich: c - p = S - PV(X)
LHS_euro = c - p
RHS_euro = S - PV_X
print(f"1. Parytet Europejski (c - p = S - PV(X)):")
print(f"   Lewa strona (c-p): {c:.4f} - {p:.4f} = {LHS_euro:.4f}")
print(f"   Prawa strona (S - X(1+R)^-N): {S} - {PV_X:.4f} = {RHS_euro:.4f}")
print(f"   Czy spelniony? {'TAK' if abs(LHS_euro - RHS_euro) < 1e-9 else 'NIE'}")

# 2. Nierówność dla opcji amerykańskich: S - X < C - P < S - PV(X)
diff_amer = C_amer - P_amer
lower_bound = S - X
upper_bound = S - PV_X

print(f"\n2. Parytet Amerykanski (S - X <= C - P <= S - PV(X)):")
print(f"   Dolna granica (S - X): {lower_bound:.4f}")
print(f"   Roznica C - P: {C_amer:.4f} - {P_amer:.4f} = {diff_amer:.4f}")
print(f"   Gorna granica (S - PV(X)): {upper_bound:.4f}")
is_satisfied = (lower_bound <= diff_amer + 1e-9) and (diff_amer <= upper_bound + 1e-9)
print(f"   Czy spelniony? {'TAK' if is_satisfied else 'NIE'}")