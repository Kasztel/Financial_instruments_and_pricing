def solve_fx_arbitrage():
    s_bid = 3.9155
    s_ask = 3.9165
    pln_bid, pln_ask = 0.0575, 0.0595
    usd_bid, usd_ask = 0.0540, 0.0550
    t = 3 / 12
    x_bid = s_bid * (1 + pln_bid * t) / (1 + usd_ask * t)
    x_ask = s_ask * (1 + pln_ask * t) / (1 + usd_bid * t)

    print(f"Computed X_BID: {x_bid:.5f}")
    print(f"Computed X_ASK: {x_ask:.5f}")

    print("\nREPLICATION STRATEGY FOR THE BANK:")
    print(f"1. To offer BID ({x_bid:.5f}):")
    print(f"   - Borrow USD @ {usd_ask * 100:.2f}%")
    print(f"   - Sell USD for PLN @ {s_bid}")
    print(f"   - Deposit PLN @ {pln_bid * 100:.2f}%")

    print(f"\n2. To offer ASK ({x_ask:.5f}):")
    print(f"   - Borrow PLN @ {pln_ask * 100:.2f}%")
    print(f"   - Buy USD for PLN @ {s_ask}")
    print(f"   - Deposit USD @ {usd_bid * 100:.2f}%")


if __name__ == "__main__":
    solve_fx_arbitrage()