from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


data=pd.read_csv('Nifty_50_list.csv')

com_code=data[['CODE']]
print(com_code)

driver=webdriver.Firefox(executable_path ='/home/shivam/Videos/Selenium_hack/geckodriver-v0.24.0-linux64/geckodriver')

link_text='https://secure.icicidirect.com/IDirectTrading/Trading/trading_stock_quote.aspx?Symbol='

for i in range(0,50):
	driver.get(link_text+com_code["CODE"][i])
	res=input(i)
	if(res=='n' or res=='N'):
		print(com_code["CODE"][i]+ " didn't work")
	else:
		continue

driver.quit()
