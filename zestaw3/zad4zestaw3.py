import numpy as np

# 1. Definicja krzywej dochodowości (ta sama co w zadaniu 3)
def y(t):
    return -0.001 * (t**2) + 0.0105 * t + 0.045

# Funkcja czynnika dyskontowego DF(t) = 1 / (1+y(t))^t
def discount_factor(t):
    if t == 0: return 1.0
    return 1.0 / ((1.0 + y(t)) ** t)

# 2. Parametry kontraktu IRS
T_maturity = 2.5      # Zapadalność: 2.5 roku
freq = 0.5            # Częstotliwość: półroczna 
payment_dates = np.arange(freq, T_maturity + 0.01, freq) # [0.5, 1.0, 1.5, 2.0, 2.5]

# 3. Funkcja wyceniająca stałą stopę IRS
# spread - marża dodawana do stopy zmiennej (np. 0.01 dla WIBOR+1%)
def calculate_irs_fixed_rate(spread):
    pv_floating = 0.0       # Wartość obecna nogi zmiennej
    pv_fixed_annuity = 0.0  # Suma czynników dyskontowych
    
    t_prev = 0.0
    for t_pay in payment_dates:
        # DF na moment płatności
        df_pay = discount_factor(t_pay)
        
        # Obliczenie stopy Forward na dany okres (WIBOR)
        # Stopa forward roczna 'f_ann' wynika z czynników dyskontowych:
        # DF(t_prev) / DF(t_pay) = (1 + f_ann)^(t_pay - t_prev)
        df_prev = discount_factor(t_prev)
        dt = t_pay - t_prev  # powinno wynosić 0.5
        
        # Forward factor = (1 + f_ann)^dt
        fwd_factor_period = df_prev / df_pay 
        
        # Roczna stopa forward (zdeannualizowana)
        f_ann = (fwd_factor_period ** (1.0/dt)) - 1.0
        
        # FLOATING
        # Stopa referencyjna = Forward + Spread
        ref_rate = f_ann + spread
        
        # Płatność za okres 0.5 roku przy kapitalizacji rocznej efektywnej:
        # Payment = (1 + ref_rate)^0.5 - 1  [źródło: 27]
        float_payment = (1.0 + ref_rate) ** dt - 1.0
        
        # Dodajemy zdyskontowaną płatność do sumy
        pv_floating += float_payment * df_pay
        
        # FIXED
        # Szukamy r_IRS. Płatność stała to również ((1+r_IRS)^0.5 - 1).
        # Sumujemy DF, by potem wyciągnąć r_IRS przed nawias.
        pv_fixed_annuity += df_pay
        
        # Przesunięcie czasu
        t_prev = t_pay
        
    # Równanie równowagi:
    # PV_Fixed = PV_Floating
    # ((1 + r_IRS)^0.5 - 1) * Suma(DF) = PV_Floating
    # (1 + r_IRS)^0.5 = (PV_Floating / Suma(DF)) + 1
    
    val_semi = (pv_floating / pv_fixed_annuity) + 1.0
    r_irs = (val_semi ** (1.0/freq)) - 1.0 # Powrót do stopy rocznej
    
    return r_irs

# 4a. WIBOR czysty (spread = 0)
irs_4a = calculate_irs_fixed_rate(0.0)
print(f"4a. IRS Rate (WIBOR):         {irs_4a:.4%} (ok. {irs_4a*100:.2f}%)")

# 4b. WIBOR + 1% (spread = 0.01)
irs_4b = calculate_irs_fixed_rate(0.01)
print(f"4b. IRS Rate (WIBOR + 1%):    {irs_4b:.4%} (ok. {irs_4b*100:.2f}%)")

# 4c. WIBOR - 1% (spread = -0.01)
irs_4c = calculate_irs_fixed_rate(-0.01)
print(f"4c. IRS Rate (WIBOR - 1%):    {irs_4c:.4%} (ok. {irs_4c*100:.2f}%)")