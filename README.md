# Algorithmic Trading Strategy & Backtesting - DecodeLabs Stock Market Project 3

## What It Does
Backtests a simple moving average crossover trading strategy over 5 years of data.

## Strategy Rules
- Entry: 50 MA crosses above 200 MA (BUY)
- Exit: 50 MA crosses below 200 MA (SELL)
- Stop Loss: -5%
- Take Profit: +10%

## Features
- Synthetic 5-year market data generation
- Moving average calculation
- Trade execution logic
- Performance metrics (win rate, return)
- Trade history display

## How to Run
1. Install: `pip install pandas numpy`
2. Run: `python trading_backtest.py`

## Author
Aiman Zahoor