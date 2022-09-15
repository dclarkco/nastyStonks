import nasdaqdatalink, re
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

apikey = ''

def getNasty(ticker, out, startDate, endDate):
	data = (nasdaqdatalink.get(ticker, start_date = startDate, end_date = endDate, api_key = apikey))
	try:
		print('\n',ticker)
		print(data.head())
	except:
		print("Dataset does not contain data...")
	if out:
		filename = 'data_{}.csv'.format(ticker.replace('/', '_'))
		print(filename)
		data.to_csv(filename)
	return data


startDate = '2000-01-01'
endDate = '2022-08-18'

search = ['FRED/GDP', 'FRED/GDPC1', 'FRED/CPIAUCSL', 'FRED/CPILFESL', 'FRED/BASE', 'FRED/M1', 'FRED/DFF', 'FRED/DGS5',
'FRED/DGS10', 'FRED/DGS30', 'FRED/T5YIE', 'FRED/DPRIME', 'FRED/UNRATE', 'FRED/NROU', 'FRED/NROUST', 'FRED/CIVPART', 'FRED/MEHOINUSA672N',
'FRED/DSPI', 'FRED/DSPIC96', 'FRED/INDPRO', 'FRED/TCU', 'FRED/HOUST', 'FRED/CP', 'FRED/STLFSI', 'FRED/GFDEBTN', 'CUR/EUR', 'CUR/CNY', 'CUR/GBP',
'ECONOMIST/BIGMAC_USA', 'ECONOMIST/BIGMAC_CHN', 'ECONOMIST/BIGMAC_EUR', 'WIKI/AAPL', 'WIKI/MSFT', 'WIKI/GOOG', 'WIKI/AMZN', 'WIKI/TSLA',
'WIKI/UNH', 'WIKI/V', 'WIKI/NVDA', 'WIKI/XOM', 'WIKI/WMT', 'WIKI/MA', 'WIKI/JPM', 'WIKI/CVX', 'WIKI/BAC', 'WIKI/DHR', 'WIKI/ORCL', 'WIKI/CSCO',
'WIKI/NKE', 'WIKI/INTC']

search = ['ECONOMIST/BIGMAC_USA', 'ECONOMIST/BIGMAC_CHN', 'ECONOMIST/BIGMAC_EUR', 'WIKI/AAPL', 'WIKI/MSFT', 'WIKI/GOOG', 'WIKI/AMZN', 'WIKI/TSLA',
'WIKI/UNH', 'WIKI/V', 'WIKI/NVDA', 'WIKI/XOM', 'WIKI/WMT', 'WIKI/MA', 'WIKI/JPM', 'WIKI/CVX', 'WIKI/BAC', 'WIKI/DHR', 'WIKI/ORCL', 'WIKI/CSCO',
'WIKI/NKE', 'WIKI/INTC']


fullDF = pd.DataFrame(columns = ["date"], index = (pd.date_range(start = startDate, end = endDate)))
for query in search:
	data = (getNasty(query, out=False, startDate = startDate, endDate = endDate))
	if len(data.columns) > 1:
		fix = str(re.sub(r'^.*?/','', query)+"_")
		data = data.add_prefix(fix)
		print(fix, len(data.columns), data.columns)

		for column in data.columns:
			fullDF = fullDF.join(data[column])
			print("Joined", column)
	else:
		print("SHORT QUERY ________________________________")
		fullDF[query] = data

print("{} Datasets downloaded...".format(len(search)))
fullDF = fullDF.drop(columns = 'date')
fullDF = fullDF.fillna(method = 'ffill')
fullDF = fullDF.fillna(method = 'bfill')

fullDF.to_csv('CEI.csv') # Combined Economic Indicators
#fullDF.to_csv('S&P.csv')

print(fullDF.head(), fullDF.describe())

