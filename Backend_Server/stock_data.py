from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv


link_text='https://secure.icicidirect.com/IDirectTrading/Trading/trading_stock_quote.aspx?Symbol='
soup=BeautifulSoup


with open('stock_data.csv','w',newline='',encoding='utf-8-sig') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerow(['NAME','LTP','DC','DO','DH','DL','PDC'])
		writeFile.close()

data=pd.read_csv('Nifty_50_list.csv')
com_code=data[['CODE']]
print(com_code['CODE'])

for i in range(0,50):
	site_html=requests.get(link_text+com_code["CODE"][i])
	bs4_html = BeautifulSoup(site_html.content, 'html5lib') 
	 
	table1=bs4_html.find('table',class_='smallfont1')
	t2=table1.find('tbody')
	data_row=t2.find_all('tr')


	ltp=data_row[1].find_all('td')[1].text.strip()
	dc=data_row[2].find_all('td')[1].text.strip()
	do=data_row[3].find_all('td')[1].text.strip()
	dh=data_row[4].find_all('td')[1].text.strip()
	dl=data_row[5].find_all('td')[1].text.strip()
	pdc=data_row[6].find_all('td')[1].text.strip()

	print(com_code["CODE"][i],ltp,dc,do,dh,dl,pdc)
		
	with open('stock_data.csv','a',newline='',encoding='utf-8-sig') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerow([com_code["CODE"][i],ltp,dc,do,dh,dl,pdc])
		writeFile.close()



