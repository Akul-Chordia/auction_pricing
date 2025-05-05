import matplotlib.pyplot as plt
import numpy as np

def generate_order_book(last_price, size=100):
    bid_prices = np.round(np.random.normal(loc=last_price * 0.98, scale=2, size=size), 2)
    ask_prices = np.round(np.random.normal(loc=last_price * 1.02, scale=2, size=size), 2)
    bid_volumes = np.abs(np.random.normal(loc=500, scale=200, size=size))
    ask_volumes = np.abs(np.random.normal(loc=500, scale=200, size=size))

    bid_book = sorted(zip(bid_prices, bid_volumes), key=lambda x: -x[0])
    ask_book = sorted(zip(ask_prices, ask_volumes), key=lambda x: x[0])

    return bid_book, ask_book

def get_auction_price(bid_book, ask_book):
    agg_orders = []

    # Cumulative bid
    cum_vol = 0
    for price, vol in bid_book:
        cum_vol += vol
        agg_orders.append(("B", price, cum_vol))

    # Cumulative ask
    cum_vol = 0
    for price, vol in ask_book:
        cum_vol += vol
        agg_orders.append(("A", price, cum_vol))

    # Sort by price to simulate auction
    agg_orders.sort(key=lambda x: x[1])

    max_volume, auction_price = 0, 0
    bid_vol, ask_vol = 0, 0
    for side, price, volume in agg_orders:
        if side == "B":
            bid_vol = volume
        else:
            ask_vol = volume
        trade_vol = min(bid_vol, ask_vol)
        if trade_vol > max_volume:
            max_volume = trade_vol
            auction_price = price

    return auction_price, max_volume

# Simulation loop
N = 1000
prices = np.empty(N+1)
volumes = np.empty(N+1)
prices[0] = 100
volumes[0] = 0

for i in range(1, N+1):
    bid_book, ask_book = generate_order_book(prices[i-1])
    auction_price, volume = get_auction_price(bid_book, ask_book)
    prices[i] = auction_price
    volumes[i] = volume

# Plotting
x = np.arange(N+1)
fig, ax1 = plt.subplots(figsize=(14, 6))

ax1.plot(x, prices, color='blue', label='Price', linewidth=1.5)
ax1.set_xlabel("Days")
ax1.set_ylabel("Price", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, linestyle='--', alpha=0.3)

ax2 = ax1.twinx()
ax2.bar(x, volumes, color='gray', alpha=0.3, width=1.0, label='Volume')
ax2.set_ylabel("Volume", color='gray')
ax2.tick_params(axis='y', labelcolor='gray')
ax2.set_yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000])
ax2.set_ylim([0, 50000])

plt.title("Auction Pricing (with Volume)")
fig.tight_layout()
plt.show()
