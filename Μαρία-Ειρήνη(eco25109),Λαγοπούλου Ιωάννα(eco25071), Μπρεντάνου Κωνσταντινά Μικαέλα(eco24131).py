import pandas as pd
from pandas_datareader import data as web
 #Define FRED series
series = [
    "FEDFUNDS",
    "CPIAUCSL",
    "UNRATE",
    "DGS10",
    "DGS2",
    "VIXCLS",
]
# Define output folder
output_folder = "../data"

# Download data
data = web.DataReader(
    series,
    "fred",
    start="2005-01-01"
)

# Convert to monthly frequency
monthly_data = data.resample("ME").last()

# Save each series in a separate CSV file
for ticker in series:
    monthly_data[[ticker]].to_csv(
        f"{output_folder}/{ticker}_monthly.csv"
    )

print("All 6 FRED CSV files saved successfully in Python_eco_project/data!")
#Fred data type validation
print(monthly_data.dtypes)
FEDFUNDS    float64
CPIAUCSL    float64
UNRATE      float64
DGS10       float64
DGS2        float64
VIXCLS      float64
dtype: object
#Check for missing values 
print(monthly_data.isna().sum())
FEDFUNDS    1
CPIAUCSL    2
UNRATE      2
DGS10       0
DGS2        0
VIXCLS      0
dtype: int64
#Check for duplicate dates 
print("Duplicate dates:", monthly_data.index.duplicated().sum())
Duplicate dates: 0
#Check for duplicate value rows
print("Duplicate rows:", monthly_data.duplicated().sum())
Duplicate rows: 0
#Outliers
Q1= monthly_data.quantile(0.25)
Q3= monthly_data.quantile(0.75)
IQR= Q3-Q1

lower_bound= Q1-1.5*IQR
upper_bound= Q3+1.5*IQR

outliers= ((monthly_data<lower_bound)|(monthly_data>upper_bound)).sum()
print("Outliers (IQR) per variable:")
print(outliers)
Outliers (IQR) per variable:
FEDFUNDS     0
CPIAUCSL     0
UNRATE       2
DGS10        0
DGS2         0
VIXCLS      12
dtype: int64
monthly_data.to_csv('fred_clean.csv')
import yfinance as yf
import pandas as pd

# Define tickers
tickers = [
    "SPY",
    "QQQ",
    "IWM",
    "AAPL",
    "NVDA",
    "TLT",
    "GLD"
]

# Define output folder
output_folder = "../data"

# Download daily data
data = yf.download(
    tickers,
    start="2005-01-01",
    auto_adjust=True
)

# Convert to monthly frequency
monthly_data = data.resample("ME").last()

# Save each ticker in a separate CSV file
for ticker in tickers:
    monthly_prices = monthly_data["Close"][ticker]

    monthly_prices.to_csv(
        f"{output_folder}/{ticker}_monthly.csv",
        header=["Close"]
    )

print("All 7 Yahoo Finance CSV files saved successfully in the data folder!")
#Yahoo finance data validation
print(monthly_data["Close"].dtypes)
Ticker
AAPL    float64
GLD     float64
IWM     float64
NVDA    float64
QQQ     float64
SPY     float64
TLT     float64
dtype: object
#Check for missing values
print(monthly_data.isna().sum())
Price   Ticker
Close   AAPL      0
        GLD       0
        IWM       0
        NVDA      0
        QQQ       0
        SPY       0
        TLT       0
High    AAPL      0
        GLD       0
        IWM       0
        NVDA      0
        QQQ       0
        SPY       0
        TLT       0
Low     AAPL      0
        GLD       0
        IWM       0
        NVDA      0
        QQQ       0
        SPY       0
        TLT       0
Open    AAPL      0
        GLD       0
        IWM       0
        NVDA      0
        QQQ       0
        SPY       0
        TLT       0
Volume  AAPL      0
        GLD       0
        IWM       0
        NVDA      0
        QQQ       0
        SPY       0
        TLT       0
dtype: int64
#Check for duplicate dates
print("Duplicate dates:", monthly_data.index.duplicated().sum())
Duplicate dates: 0
#Check for duplicate value rows
print("Duplicate rows:", monthly_data.duplicated().sum())
Duplicate rows: 0
#Outliers
Q1= monthly_data.quantile(0.25)
Q3= monthly_data.quantile(0.75)
IQR=Q3-Q1

lower_bound=Q1-1.5*IQR
upper_bound=Q3+1.5*IQR

outliers= ((monthly_data<lower_bound)|(monthly_data>upper_bound)).sum()
print("Outliers (IQR) per variable:")
print(outliers)
Outliers (IQR) per variable:
Price   Ticker
Close   AAPL       5
        GLD       22
        IWM        0
        NVDA      43
        QQQ        8
        SPY        0
        TLT        0
High    AAPL       4
        GLD       22
        IWM        0
        NVDA      43
        QQQ        8
        SPY        1
        TLT        0
Low     AAPL       5
        GLD       23
        IWM        0
        NVDA      43
        QQQ        8
        SPY        2
        TLT        0
Open    AAPL       4
        GLD       22
        IWM        0
        NVDA      43
        QQQ        8
        SPY        2
        TLT        0
Volume  AAPL      13
        GLD       11
        IWM       16
        NVDA       6
        QQQ       18
        SPY       21
        TLT       31
dtype: int64
monthly_data.to_csv('yf_clean.csv')
#Loading the files
df_yahoo= pd.read_csv('yf_clean.csv', index_col=0, parse_dates=True)
df_fred= pd.read_csv('fred_clean.csv', index_col=0, parse_dates=True)
#Definition of valid dates
idx_yahoo= pd.to_datetime(df_yahoo.index, errors='coerce').dropna()
idx_fred= pd.to_datetime(df_fred.index, errors='coerce').dropna()
#Finding non-common dates
non_common_dates=idx_yahoo.symmetric_difference(idx_fred)
#Results
print(f"Total non-common dates: {len(non_common_dates)}")
display(non_common_dates)
Total non-common dates: 0
DatetimeIndex([], dtype='datetime64[us]', freq=None)
#Check for potential inconsistencies
print("Negative prices on Yahoo:\n", (df_yahoo.select_dtypes(include='number') < 0).sum())
print("Negative prices in Fred:\n", (df_fred.select_dtypes(include='number') < 0).sum())
Negative prices on Yahoo:
 Series([], dtype: float64)
Negative prices in Fred:
 FEDFUNDS    0
CPIAUCSL    0
UNRATE      0
DGS10       0
DGS2        0
VIXCLS      0
dtype: int64
