import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(years=5, start_price=100, volatility=0.02):
    np.random.seed(42)
    days = years * 252
    start_date = datetime(2021, 1, 1)
    
    returns = np.random.normal(0.0005, volatility, days)
    price = start_price * np.exp(np.cumsum(returns))
    
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    df = pd.DataFrame({
        'Date': dates,
        'Close': price,
        'High': price * (1 + np.random.uniform(0, 0.02, days)),
        'Low': price * (1 - np.random.uniform(0, 0.02, days)),
        'Open': price * (1 + np.random.uniform(-0.01, 0.01, days))
    })
    
    return df

def calculate_moving_averages(df, short_window=50, long_window=200):
    df['MA50'] = df['Close'].rolling(window=short_window).mean()
    df['MA200'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = 0
    df.loc[df['MA50'] > df['MA200'], 'Signal'] = 1
    df.loc[df['MA50'] <= df['MA200'], 'Signal'] = -1
    return df

def backtest_strategy(df, initial_capital=10000, stop_loss=0.05, take_profit=0.10):
    capital = initial_capital
    position = 0
    trades = []
    entry_price = 0
    daily_returns = []
    
    df = df.copy()
    df['Position'] = 0
    
    for i in range(len(df)):
        if pd.isna(df.loc[i, 'Signal']):
            continue
        
        signal = df.loc[i, 'Signal']
        price = df.loc[i, 'Close']
        
        if position == 0 and signal == 1:
            shares = capital // price
            if shares > 0:
                position = shares
                entry_price = price
                capital -= shares * price
                trades.append({
                    'Date': df.loc[i, 'Date'],
                    'Type': 'BUY',
                    'Price': price,
                    'Shares': shares,
                    'Capital': capital
                })
        
        elif position > 0:
            profit_pct = (price - entry_price) / entry_price
            
            if signal == -1 or profit_pct <= -stop_loss or profit_pct >= take_profit:
                capital += position * price
                trades.append({
                    'Date': df.loc[i, 'Date'],
                    'Type': 'SELL',
                    'Price': price,
                    'Shares': position,
                    'Capital': capital,
                    'Profit_Pct': profit_pct
                })
                position = 0
                entry_price = 0
    
    if position > 0:
        price = df.iloc[-1]['Close']
        capital += position * price
        trades.append({
            'Date': df.iloc[-1]['Date'],
            'Type': 'SELL (Final)',
            'Price': price,
            'Shares': position,
            'Capital': capital,
            'Profit_Pct': (price - entry_price) / entry_price if entry_price else 0
        })
    
    total_return = (capital - initial_capital) / initial_capital * 100
    num_trades = len([t for t in trades if t['Type'] == 'BUY'])
    winning_trades = len([t for t in trades if t.get('Profit_Pct', 0) > 0])
    win_rate = winning_trades / num_trades * 100 if num_trades > 0 else 0
    
    return {
        'final_capital': capital,
        'total_return': total_return,
        'trades': trades,
        'num_trades': num_trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate
    }

def analyze_performance(results):
    print("\n" + "=" * 60)
    print("   BACKTEST RESULTS")
    print("=" * 60)
    print(f"Initial Capital: $10,000.00")
    print(f"Final Capital: ${results['final_capital']:,.2f}")
    print(f"Total Return: {results['total_return']:.2f}%")
    print(f"Number of Trades: {results['num_trades']}")
    print(f"Winning Trades: {results['winning_trades']}")
    print(f"Win Rate: {results['win_rate']:.2f}%")
    
    if results['total_return'] > 0:
        print("\n✅ Strategy shows a positive return!")
    else:
        print("\n⚠️ Strategy shows a negative return. Consider optimizing.")
    
    print("\nTrade History:")
    print("-" * 60)
    print(f"{'Date':<12} {'Type':<12} {'Price':<10} {'Shares':<8} {'Profit':<10}")
    print("-" * 60)
    
    for trade in results['trades'][-10:]:
        profit = trade.get('Profit_Pct', 0)
        profit_str = f"{profit*100:.1f}%" if profit else "0%"
        print(f"{str(trade['Date'])[:10]:<12} {trade['Type']:<12} {trade['Price']:.2f}   {trade['Shares']:<8} {profit_str:<10}")
    
    print("-" * 60)

def main():
    print("\n" + "=" * 60)
    print("   ALGORITHMIC TRADING STRATEGY & BACKTESTING")
    print("=" * 60)
    
    print("\n[1] Generating 5 Years of Synthetic Market Data...")
    df = generate_synthetic_data(years=5)
    print(f"✅ Generated {len(df)} trading days")
    
    print("\n[2] Calculating Moving Averages (50 & 200 day)...")
    df = calculate_moving_averages(df)
    print("✅ Moving averages calculated")
    
    print("\n[3] Strategy Rules:")
    print("-" * 40)
    print("Entry: When 50 MA crosses above 200 MA (BUY)")
    print("Exit: When 50 MA crosses below 200 MA (SELL)")
    print("Stop Loss: -5%")
    print("Take Profit: +10%")
    print("-" * 40)
    
    print("\n[4] Running Backtest...")
    results = backtest_strategy(df)
    
    analyze_performance(results)
    
    print("\n" + "=" * 60)
    print("   BACKTESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()