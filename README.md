# Python-RTFD
A Python-based command line tool that queries the [Real Time Finance Data API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-finance-data) (courtesy of RapidAPI) and retrieves news articles, information on stock/ETF performance, company balance sheets, income statements, and cash flows, as well as the exchange rate between two currencies, and displays a graph of the data using matplotlib which can be saved.

## Requirements
I designed this tool with Python 3.10.3056.0. This isn't to say that older versions of Python 3 might not be able to run this tool, but please bear it in mind.

Ensure the following libraries are installed as they are needed to run the tool:
- requests
- pandas
- matplotlib

**Additionally**, **you will need to replace the `X-RapidAPI-Key` value on line 11 with your own through RapidAPI**.

## Usage
The tool will always start with: `python rtfd02.py`
From there, you can select different options.

### Market Trends
`python rtfd02.py trends <trend> <2-letter country code>`

Supported `<trend>` parameters, per the API documentation, are:
- `MARKET_INDEXES` 
- `MOST_ACTIVE`
- `GAINERS` 
- `LOSERS` 
- `CRYPTO`
- `CURRENCIES`
- `CLIMATE_LEADERS`

A comprehensive list of the Alpha 2 country codes, used for `<2-letter country code>` can be found on [iban.org/country-codes](https://www.iban.com/country-codes)

### Stocks
`python rtfd02.py stocks <ticker> <time series>`

Supported `<time series>` parameters, per the API documentation, retrieve historical information starting from today's date:
- `1D`
- `5D`
- `1M`
- `5M`
- `YTD`
- `1Y`
- `5Y`
- `MAX`

### Company Statements
`python rtfd02.py company income/balance/cf <ticker> <period>`

Supported `<period>` parameters, per the API documentation, retrieve historical information starting from today's date:
- `ANNUAL`
- `QUARTERLY`

**Income Statements**: `python rtfd02.py company income <ticker> <period>`

**Balance Sheets**: `python rtfd02.py company balance <ticker> <period>`

**Cash Flows**: `python rtfd02.py company cf <ticker> <period>`

### Currency Exchanges/Change Over Time
`python rtfd02.py exchange <currency1> <currency2> <time series>`

Currency parameters must be denoted using their 3-letter code.
- US Dollar: `USD`
- British Pound Sterling: `GBP`
- Bitcoin: `BTC`
- Ethereum: `ETH`

Supported `<time series>` parameters are the same as under Stocks
