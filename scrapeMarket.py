
import requests, pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import sys

sys.path.insert(0, "")


# scrapeMarket.py
# Dillon Clark, Godirect Financial 2022
# retreives LIBOR data from WSJ each week

# TODO:
# send email with csv and readable data


URL = ("https://www.wsj.com/market-data/bonds")

def getIngredients(URL):

	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
		} # spoof a macOS device to breach blockers

	page = requests.get(URL, headers = headers)
	return page

def getLIBOR(URL, toCSV, send):

	page = getIngredients(URL)

	soup = BeautifulSoup(page.content, "html.parser")

	table = soup.find_all("td", class_="WSJTables--table__cell--2u6629rx")
	index = soup.find_all("th", class_="WSJTables--thead__cell--1Do0eEYL")

	#ids = [tag['id'] for tag in soup.select('div[id]')] # --- List all IDs

	LIBORdic = {}
	LIBORlis = []

	for spoon in table:
		print(spoon.text)
		LIBORlis.append(spoon.text)

	LIBORdic = {"Index":["Latest", "1wk ago", "High", "Low"], LIBORlis[0]:LIBORlis[1:5], LIBORlis[5]:LIBORlis[6:10], LIBORlis[10]:LIBORlis[11:15], LIBORlis[15]:LIBORlis[16:20], LIBORlis[20]:LIBORlis[21:25]}

	LIBORdf = pd.DataFrame(LIBORdic)
	#LIBORdf = LIBORdf.set_index("Timeline")

	print(LIBORdf.head())

	if(toCSV):
		LIBORdf.to_csv("LIBOR_{}.csv".format(datetime.now().strftime("%m-%d-%y")))

	if(send):
		sendLIBOR(LIBORdf)

	return LIBORdf


def sendLIBOR(LIBORdf):
	import emailFiles

	receiver = "dillon@poweredbyqed.com"
	sender = "pigbotqed@gmail.com"
	subject = "LIBOR rates {}".format(datetime.now().strftime("%m-%d-%y"))
	message = ["LIBOR rates: {}".format(datetime.now().strftime("%m-%d-%y")), LIBORdf]
	attach = "LIBOR_{}.csv".format(datetime.now().strftime("%m-%d-%y"))

	emailFiles.send_mail(toaddr = receiver, subject = subject, message = message, attach = attach)
	print('Mail sent to:', receiver, "complete...")

getLIBOR(URL, toCSV = True, send = False)


