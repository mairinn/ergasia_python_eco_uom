import pandas as pd
import os

# Create directory for raw CSV files
output_dir = "data/raw_data"
os.makedirs(output_dir, exist_ok=True)

# FRED series
series = [
    "FEDFUNDS",
    "CPIAUCSL",
    "UNRATE",
    "DGS10",
    "DGS2",
    "VIXCLS",
    "BAMLH0A0HYM2"
]

# Download and save each series
for ticker in series:

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={ticker}"

    df = pd.read_csv(url)

    # Save CSV file
    output_path = os.path.join(output_dir, f"{ticker}.csv")
    df.to_csv(output_path, index=False)

    print(f"{ticker} downloaded successfully!")

print("All FRED downloads completed!")
