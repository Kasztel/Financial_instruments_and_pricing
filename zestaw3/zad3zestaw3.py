import numpy as np

# 1. Definicja krzywej dochodowości zero-coupon y(t)
# y(t) = -0.001*t^2 + 0.0105*t + 0.045
# Funkcja zwraca wartość w ułamku dziesiętnym (np. 0.045 to 4.5%)
def y(t):
    return -0.001 * (t**2) + 0.0105 * t + 0.045

# 2. Funkcja pomocnicza: Obliczanie stopy FRA (Forward)
# Oblicza stopę terminową między czasem t1 a t2 na podstawie krzywej y(t)
# Wzór wynika z braku arbitrażu: (1+y(t2))^t2 = (1+y(t1))^t1 * (1+fra)^(t2-t1)
def calculate_fra_rate(t1, t2, curve_func=y):
    # Wartość pieniądza w czasie (FV) dla t1 i t2
    fv_t2 = (1.0 + curve_func(t2)) ** t2
    fv_t1 = (1.0 + curve_func(t1)) ** t1
    
    # Czas trwania kontraktu FRA
    dt = t2 - t1
    
    # Wyznaczenie stopy forward (rocznej, efektywnej)
    fwd = (fv_t2 / fv_t1) ** (1.0 / dt) - 1.0
    return fwd

# Punkt 3a
# Oblicz stałą stopę dla kontraktu FRA "1y x 1.5y"
# t1 = 1.0 rok (start), t2 = 1.5 roku (koniec)
fra_3a = calculate_fra_rate(1.0, 1.5)
print(f"3a. Kurs FRA '1y x 1.5y' (start za rok): {fra_3a:.4%} (ok. {fra_3a*100:.2f}%)")


# Punkt 3b
# Oblicz oczekiwaną krzywą terminową za 0.5 roku: y_0.5(tau)
# Jest to stopa spot, jaką rynek przewiduje "dzisiaj" na moment za pół roku.
# tau - czas od momentu "za pół roku"
def y_expected_in_05(tau):
    # Czas całkowity z perspektywy "dzisiaj"
    t_total = 0.5 + tau
    
    # Matematyczna relacja stóp forward:
    fv_total = (1.0 + y(t_total)) ** t_total
    fv_05 = (1.0 + y(0.5)) ** 0.5
    
    # Wyliczenie implikowanej stopy spot na okres tau (zaczynający się w t=0.5)
    val = (fv_total / fv_05) ** (1.0 / tau) - 1.0
    return val

# Przykładowe sprawdzenie dla tau=0.5 (czyli forward 0.5 > 1.0 z perspektywy dzisiaj)
y_05_check = y_expected_in_05(0.5)
print(f"3b. Oczekiwana stopa spot za 0.5 roku (na okres 6M): {y_05_check:.4%}")


# Punkt 3c
# Założenie: Minęło 0.5 roku. Rynek miał rację, obecna krzywa to y_expected_in_05.
# Kontrakt z pkt 3a (1y x 1.5y) teraz startuje za 0.5 roku i kończy za 1.0 rok.
# t1_new = 0.5, t2_new = 1.0
fra_3c = calculate_fra_rate(0.5, 1.0, curve_func=y_expected_in_05)
print(f"3c. Wycena starego FRA po uplywie 0.5 roku (t1=0.5, t2=1.0): {fra_3c:.4%}")


# Punkt 3d
# Scenariusze: Krzywa rynkowa różni się od oczekiwanej o +/- 0.001

# Scenariusz wzrostu krzywej
def curve_up(t):
    return y_expected_in_05(t) + 0.001

# Scenariusz spadku krzywej
def curve_down(t):
    return y_expected_in_05(t) - 0.001

fra_3d_up = calculate_fra_rate(0.5, 1.0, curve_func=curve_up)
fra_3d_down = calculate_fra_rate(0.5, 1.0, curve_func=curve_down)

print(f"3d. Kurs FRA przy wzroscie krzywej o 0.1%: {fra_3d_up:.4%}")
print(f"3d. Kurs FRA przy spadku krzywej o 0.1%: {fra_3d_down:.4%}")