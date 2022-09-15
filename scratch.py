debug = True

def sendNotification():

	import os
	from datetime import datetime

	message = "Cron Test: {}".format(datetime.now().strftime("%H:%M"))
	title = "Notifcation Test"
	command = f'''
	osascript -e 'display notification "{message}" with title "{title}"'
	'''

	os.system(command)

def NastyDaqOG():
	import nasdaqdatalink as nasty

	quandl.ApiConfig.api_key = ''
	quandl.get('ECONOMIST/BIGMAC_ROU', start_date='2022-01-31', end_date='2022-01-31')

def calculateStonkReturns():
	import pandas as pd

	path = ''

	years = {1:['01/01/2021', '12/31/2021'],5:['01/01/2017', '12/31/2021'],10:['01/01/2011', '12/31/2021'],
	 15:['01/01/2006', '12/31/2021'],20:['01/01/2001', '12/31/2021']}

	#yearsDF = pd.to_datetime(pd.DataFrame(years), format = "%d/%m/%Y")

	df = pd.read_csv(path)
	df['Date'] = pd.to_datetime(df['Date'], format = "%m/%d/%Y")
	df = df.set_index(df['Date'])
	#df = df.drop('Date')

	#print(yearsDF.head())
	#print(type(df['Date'][1]))
	#print(type(df.index.values[0]))

	for i, year in years.items():
	# 	print(i, year[0], year[1])
	# 	print(df.loc[year[0],'Close/Last'])
		start = pd.Timestamp(pd.to_datetime(year[0], format = "%m/%d/%Y"))
		end = pd.Timestamp(pd.to_datetime(year[1], format = "%m/%d/%Y"))

		print(type(start), type(df['Date'][1]))
		print(start, df['Date'][1])

		# data = df.where(df['Date'] == year[0])
		# print(data)

		print(df[start])

calculateStonkReturns()
