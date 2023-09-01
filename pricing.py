import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mplcursors

# Defining the variables
s_0 = 100
rf = .05
volatility = .2
strike_price = 110
barrier = 130
maturity = 365
mc_iterations = 100
seed = 1234

#setting the random seed
#np.random.seed(seed)

# defining the stock S function which follows a geometric Brownian motion
def Brownian_motion(stock_price, drift, volatility, maturity):
    b_motion = np.random.randn()
    delta_t = 1/maturity
    dS = drift*stock_price*delta_t + volatility*stock_price*b_motion*np.sqrt(delta_t)
    return dS

# defining the simulation function to get the daily prices of the stock
def full_path(s_0, drift, volatility, maturity):
    stock_path = [s_0]
    for i in range(maturity):
        dS = Brownian_motion(stock_path[i], rf, volatility, maturity)
        stock_path.append(stock_path[i] + dS)
    return stock_path

def path_pricing(stock_path, barrier, strike_price):
    if max(stock_path) >= barrier or stock_path[-1] < strike_price:
        return 0
    return stock_path[-1] - strike_price

# defining the monte carlo simulation function
def monte_carlo(s_0, drift, volatility, maturity, barrier, strike_price, mc_iterations):
    paths = []
    prices = []
    for i in range(mc_iterations):
        path = full_path(s_0, drift, volatility, maturity)
        path_price = path_pricing(path, barrier, strike_price)
        paths.append(path)
        prices.append(round(path_price,2))
    return prices, paths

price_simulation, paths_simulation = monte_carlo(s_0, rf, volatility, maturity, barrier, strike_price, mc_iterations)

discounted_prices = []
for price in price_simulation:
    d_price = price * (1 + rf) ** -1
    discounted_prices.append(d_price)

average_price = sum(discounted_prices) / len(discounted_prices) 
print(f'The barrier option price is: {average_price}')

""" This commented part of the code is to get a non-animated plot
# plotting the results
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

fig, ax = plt.subplots(figsize=(20, 12))
ax.axhline(y=barrier, color='r', linestyle='--', label='Barrier')
ax.axhline(y=strike_price, color='g', linestyle='--', label='Strike Price')

# differentiate the colors of the paths with positive option price

negative_end_color = 'lightblue'

for i in range(len(paths_simulation)):
    path = paths_simulation[i]
    option_price = price_simulation[i]
    if option_price == 0:
        plt.plot(path, color=negative_end_color, alpha=0.25)
    else:
        plt.plot(path)

# Adjust x-ticks
xticks = np.arange(0, maturity + 1, 50)
xticks[-1] = maturity  # Ensure the last tick is exactly 365
plt.xticks(xticks)


plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.title('Monte Carlo Simulated Stock Paths')
plt.legend()


plt.show()"""

# plotting the results in an animated plot
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

fig, ax = plt.subplots(figsize=(20, 12))

# Set y-axis limits first to ensure proper positioning of horizontal lines.
ax.set_ylim(60, 180)
yticks = np.arange(60, 180, 10)  # every 10 units from 60 to 180
ax.set_yticks(yticks)

# Then, plot the barrier and strike price lines.
ax.axhline(y=barrier, color='#18c0c4', linestyle='-.', label='Barrier', zorder = 101, linewidth=2.5)
ax.axhline(y=strike_price, color='#f62196', linestyle='-.', label='Strike Price', zorder = 101, linewidth=2.5)

negative_end_color = 'lightblue'

# Set up lines for animation
lines = [ax.plot([], [], lw=2, alpha=0.25 if price_simulation[i] == 0 else 1)[0] for i in range(mc_iterations)]

def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Define the number of days to skip in each frame for smoother transition.
days_skip = 1

# dynamic text for days counting
day_text = ax.text(0.93, 0.85, '', transform=ax.transAxes, fontsize=20, fontweight='bold')

def update(frame):
    frame *= days_skip
    for i, line in enumerate(lines):
        line.set_data(range(frame + 1), paths_simulation[i][:frame + 1])
        if price_simulation[i] == 0:
            line.set_color(negative_end_color)
            line.set_alpha(0.2)
    day_text.set_text(f"Day: {frame}")  
    ax.set_xlim(0, maturity)    
    return (*lines, day_text)


# Adjust x-ticks
xticks = np.arange(0, maturity + 1, 50)
xticks[-1] = maturity
ax.set_xticks(xticks)

plt.xlabel('Days', fontsize=15, fontweight='bold')
plt.ylabel('Stock Price', fontsize=15,fontweight='bold')
title_obj = plt.title('Barrier option pricing using Monte Carlo simulation', fontsize=20, fontweight='bold')
title_obj.set_position([0.5, 0.92]) 
plt.legend()


ani = FuncAnimation(fig, update, frames=range(0, maturity//days_skip + 1), init_func=init, blit=True, interval=10, repeat_delay=3000, repeat = False)

plt.tight_layout()
plt.show()

from matplotlib.animation import PillowWriter  # for GIF

# Assuming anim is your FuncAnimation object
ani.save('animation.mp4', writer='ffmpeg', fps=60)