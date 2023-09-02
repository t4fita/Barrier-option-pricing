# Barrier-option-pricing
Geometric Brownian Motion modeled stock &amp; Monte Carlo simulation in Python

This repository contains a Python implementation of the Monte Carlo simulation method for barrier option pricing. Using this approach, we can visualize simulated stock paths, taking into account various financial parameters.

## Features

- Monte Carlo simulation for stock price paths.
- Animated visualization of stock paths.
- Interactive plot allowing users to hover over paths to view option prices.
- Dynamic display of days passed in the animation.
- Barrier and strike price visualization on the graph.

## Prerequisites

- Python 3.8+
- `matplotlib`
- `numpy`
- `ffmpeg` (For saving the animation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/t4fita/Barrier-option-pricing
2. Install the required packages (it's recommended to use a virtual environment):
   ```bash
   pip install -r requirements.txt
3. Usage
   To run the simulation and visualize the animated plot:
   ```bash
    python main.py

## Configuration

The simulation's parameters like initial stock price, volatility, strike price, barrier price, maturity, etc., are adjustable within the main.py script.

## Output

The script will display an animated plot showing the simulated stock paths. You can hover over the paths to view their respective option prices.

https://github.com/t4fita/Barrier-option-pricing/assets/132291982/0d08ccb6-e636-48e9-a737-6edd92f8632a



## Saving The Animation

To save the animation, uncomment the respective lines in the main.py script. You can save it in formats like MP4 or GIF.

## License

This project is open source and available under the MIT License


