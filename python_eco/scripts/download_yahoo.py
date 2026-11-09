import yfinance as yf
import os

# Create directory for raw CSV files
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

# Yahoo Finance assets
tickers = [
    "SPY",
    "QQQ",
    "IWM",
    "AAPL",
    "NVDA",
    "TLT",
    "GLD"
]

# Download and save each asset
for ticker in tickers:

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={ticker}"

    df = yf.download(
        ticker,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        print(f"Warning: No data found for {ticker}")
        continue

    # Save CSV file
    output_path = os.path.join(output_dir, f"{ticker}.csv")
    df.to_csv(output_path, index=False)

    print(f"{ticker} downloaded successfully!")

print("All Yahoo Finance downloads completed!")
