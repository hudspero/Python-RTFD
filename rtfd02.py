#VERSION 0.2

import requests
import sys
import pandas as pd
import matplotlib.pyplot as plt

#GLOBALS
base_url = "https://real-time-finance-data.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "<insert_key_here>",
	"X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
}

#SENDING HTTP REQUEST
def http_request(endpoint, querystring):
	url = base_url + endpoint
	response = requests.request("GET", url, headers=headers, params=querystring)
	return response.json()['data']

#NEWS ARTICLE DISPLAYS
def news_handler(news):
	for article in news:
		print("")
		print("Source: {}".format(article['source']))
		print("Title: {}".format(article['article_title']))
		print("URL: {}".format(article['article_url']))
		print("")

#DATA VISUALIZATION
def time_series_plot(arg, data, argv):
	if (arg == 'stock'):
		table = pd.DataFrame.from_dict(data['time_series'], orient='index')
		plt.plot(table.price, label='Stock Price')
	elif (arg == 'income'):
		table = pd.DataFrame(data['income_statement']).iloc[::-1]
		plt.plot(table.revenue, label='Revenue')
		plt.plot(table.operating_expense, label='Operating Expenses')
		plt.plot(table.net_income, label='Net Income')
		plt.plot(table.EBITDA, label='EBITDA')
		plt.gca().invert_xaxis()
		print(table)
	elif (arg == 'balance'):
		table = pd.DataFrame(data['balance_sheet']).iloc[::-1]
		plt.plot(table.total_assets, label='Total Assets')
		plt.plot(table.total_liabilities, label='Total Liabilities')
		plt.plot(table.total_equity, label='Total Equity')
		plt.plot(table.shares_outstanding, label='Shares Outstanding')
		plt.gca().invert_xaxis()
		print(table)
	elif (arg == 'cf'):
		table = pd.DataFrame(data['cash_flow']).iloc[::-1]
		plt.plot(table.net_income, label='Net Income')
		plt.plot(table.cash_from_operations, label='CFO')
		plt.plot(table.cash_from_investing, label='CFI')
		plt.plot(table.cash_from_financing, label='CFF')
		plt.plot(table.free_cash_flow, label='FCF')
		plt.plot(table.net_change_in_cash, label='Net Change in Cash')
		plt.gca().invert_xaxis()
		print(table)
	elif (arg == 'exchange'):
		table = pd.DataFrame.from_dict(data['time_series'], orient='index')
		plt.plot(table.exchange_rate, label='A to B Exchange Rate')
		print(table)
	plt.legend()
	plt.title(argv)
	plt.show()

#INVALID INPUT CANNED RESPONSE
def invalid_input_msg():
	print("Supported format:")
	print("python3 rtfd02.py <arguments>")
	print("-   News on market trends:")
	print("--    'trends <trend> <2-letter country code>'")
	print("---      Supported trends: MARKET_INDEXES, MOST_ACTIVE, GAINERS, LOSERS, CRYPTO, CURRENCIES, CLIMATE_LEADERS")
	print("-   Stock tickers & time series:")
	print("--    'stocks <stock ticker> <time series>'")
	print("---      Supported time series: 1D, 5D, 1M, 6M, YTD, 1Y, 5Y, MAX")
	print("-   Company income statements:")
	print("--    'company income <stock ticker> <period>'")
	print("---      Supported periods: QUARTERLY, ANNUAL")
	print("-   Company balance sheets:")
	print("--    'company balance <stock ticker> <period>'")
	print("---      Supported periods: QUARTERLY, ANNUAL")
	print("-   Company cash flow:")
	print("--    'company cf <stock ticker> <period>'")
	print("---      Supported periods: QUARTERLY, ANNUAL")
	print("-   Global FIAT currency & cryptocurrency exchange rates:")
	print("--    'exchange <currency1> <currency2> <time series>'")
	print("---      Supported time series: 1D, 5D, 1M, 6M, YTD, 1Y, 5Y, MAX")

#COMMAND LINE ARGUMENTS HANDLER
if (len(sys.argv) > 1):
	if (len(sys.argv) > 2 and sys.argv[1] == 'trends'):
		if (len(sys.argv) > 3 and sys.argv[2] in ['MARKET_INDEXES', 'MOST_ACTIVE', 'GAINERS', 'LOSERS', 'CRYPTO', 'CURRENCIES', 'CLIMATE_LEADERS'] and sys.argv[3]):
			querystring = {"trend_type": sys.argv[2], "country": sys.argv[3], "language": "en"}
			news = http_request("market-trends", querystring)['news']
			news_handler(news)
		else:
			invalid_input_msg()
	elif (len(sys.argv) > 2 and sys.argv[1] == 'stocks'):
		if (len(sys.argv) > 3 and sys.argv[3] in ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']):
			querystring = {"symbol": sys.argv[2], "period": sys.argv[3], "language": "en"}
			stock = http_request("stock-time-series", querystring)
			time_series_plot('stock', stock, sys.argv)
		else:
			invalid_input_msg()
	elif (len(sys.argv) > 2 and sys.argv[1] == 'company'):
		if (len(sys.argv) > 3 and sys.argv[2] in ['income', 'balance', 'cf'] and sys.argv[4] in ['QUARTERLY', 'ANNUAL']):
			querystring = {"symbol": sys.argv[3], "period": sys.argv[4], "language": "en"}
			if (sys.argv[2] == 'income'):
				statement = http_request("company-income-statement", querystring)
				time_series_plot('income', statement, sys.argv)
			elif (sys.argv[2] == 'balance'):
				sheet = http_request("company-balance-sheet", querystring)
				time_series_plot('balance', sheet, sys.argv)
			elif (sys.argv[2] == 'cf'):
				flow = http_request("company-cash-flow", querystring)
				time_series_plot('cf', flow, sys.argv)
			else:
				invalid_input_msg()
		else:
			invalid_input_msg()
	elif (len(sys.argv) > 2 and sys.argv[1] == 'exchange'):
		if (len(sys.argv) > 4 and sys.argv[4] in ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']):
			querystring = {"from_symbol": sys.argv[2], "to_symbol": sys.argv[3], "period": sys.argv[4], "language": "en"}
			comparison = http_request("currency-time-series", querystring)
			time_series_plot('exchange', comparison, sys.argv)
		else:
			invalid_input_msg()
	else:
		invalid_input_msg()
else:
	invalid_input_msg()