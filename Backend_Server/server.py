import requests
from datetime import datetime
from datetime import timedelta
import json 
from flask import Flask, escape, request 
from pytz import timezone
import time
import sys
import csv
import random

app = Flask(__name__)
com_code=['BSESEN','HDFBAN', 'RELPET', 'HDFC', 'INFTEC', 'ICIBAN', 'ITC', 'TCS', 'KOTMAH', 'LARTOU', 'HINLEV', 'AXIBAN', 'STABAN', 'BAJFI', 'MARUTI', 'INDBA', 'ASIPAI', 'BHAAIR', 'HCLTEC', 'TITIND', 'MAHMAH', 'BAFINS', 'NTPC', 'NESIND', 'POWGRI', 'ULTCEM', 'TECMAH', 'SUNPHA', 'ONGC', 'BAAUTO', 'BHARAS', 'INDOIL', 'COALIN', 'WIPRO', 'HERHON', 'BRIIND', 'UNIP', 'DRREDD', 'ADAPOR', 'GRASIM', 'VEDLIM', 'HINDAL', 'TATSTE', 'EICMOT', 'GAIL', 'JSWSTE', 'BHAINF', 'CIPLA', 'TATMOT', 'ZEEENT', 'YESBAN']

def dayDiff(dh,dl):
	df=dh-dl
	if(df>0):
		df=1
	elif(df==0):
		df=0
	elif(df<0):
		df=-1	
	return df

def previousDayDiff(pdc, do):
	pdf=pdc-do
	if(pdf>0):
		pdf=1
	elif(pdf==0):
		pdf=0
	elif(pdf<0):
		pdf=-1	
	return pdf

def currentDayDiff(ltp, do):
	cdf=ltp-do
	if(cdf>0):
		cdf=1
	elif(cdf==0):
		cdf=0
	elif(cdf<0):
		cdf=-1	
	return cdf

def fiftyTwoWeek(ftl, pt):
	if(stockReturn>ftl and stockReturn<(ftl+.1*ftl)):
		stockReturn=1
	else:
		stockReturn=-1	
	return stockReturn

def top_5():
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
		index = i - 51
		readFile.close()

	per = []
	code = []
	inc = []
	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(index+1,index+51):
			row = dict(reader[i])
			dh=float(row["DH"])
			dl=float(row["DL"])
			pdc=float(row["PDC"])
			do=float(row["DO"])
			ltp=float(row["LTP"])
			com_name=str(row["NAME"])
			
			df=dayDiff(dh=dh,dl=dl)
			pdf=previousDayDiff(pdc=pdc,do=do)
			cdf=currentDayDiff(ltp=ltp,do=do)
			code.append(com_name)
			per.append(df+pdf+cdf) 
			inc.append((ltp - do)/ltp)
			# print(com_name, (ltp - do)/ltp * 100,df+pdf+cdf)
			
		readFile.close()

	for i in range(len(inc)):
		for j in range(i + 1, len(inc)):

			if inc[i] > inc[j]:
				inc[i], inc[j] = inc[j], inc[i]
				code[i], code[j] = code[j], code[i]
				per[i], per[j] = per[j], per[i]

	
	# for i in range(len(per)):
		# print(per[i],inc[i],code[i])

	count = 0
	codes = []

	for i in range(len(per)-1, -1, -1):
		if(per[i] == 3 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == 2 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == 1 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == 0 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == -1 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	# print(codes)

	top_5_stocks = []
	for i in range(index+1,index+51):
		row = dict(reader[i])
		com_name=str(row["NAME"])
		for j in range(5):
			if(codes[j] ==com_name):
				code_index = com_code.index(com_name)
				graph_values = []
				time_values = []
				k=0
				with open('new_stock_data.csv','r',newline='',encoding='utf-8-sig') as readFile:
					reader_graph = list(csv.DictReader(readFile))
					l = len(list(reader_graph))
					for i in range(code_index,l,51):
						row = dict(reader_graph[i])
						date_time=row["DATE_TIME"]
						name=row["NAME"]
						ltp=row["LTP"]
						dummydate = datetime.date(datetime.now())
						diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
						if(diff1.total_seconds() < 0):
							break
						else:
							if(k != 1):
								graph_values.append(row["DO"])
								call_time = datetime.strptime(date_time,format)
								m = call_time.minute
								s = ""
								if(m<10):
									s = "0" + str(m)
								else: 
									s = str(m)
								time_val = str(call_time.hour) + ":" + s
								time_values.append(time_val)
								k = 1
							graph_values.append(ltp)
							call_time = datetime.strptime(date_time,format)
							m = call_time.minute
							s = ""
							if(m<10):
								s= "0" + str(m)
							else: 
								s = str(m)
							time_val = str(call_time.hour) + ":" + s
							time_values.append(time_val)
					readFile.close()
					st_5 = row
					st_5["graph_values"] = graph_values
					st_5["time_values"] = time_values
				top_5_stocks.append(st_5)

	return(top_5_stocks)


def search_stock(search_code):
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M:%S"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max
	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
		index = i - 51
		readFile.close()
	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(index+1,index+51):
			row = dict(reader[i])
			com_name=str(row["NAME"])
			if(com_name == search_code):
				code_index = com_code.index(search_code)
				# print(code_index)	
				st_search = row
				break
		readFile.close()
	code_index = com_code.index(search_code)
	graph_values = []
	time_values = []
	k=0
	with open('new_stock_data.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader_graph = list(csv.DictReader(readFile))
		l = len(list(reader_graph))
		for i in range(code_index,l,51):
			row = dict(reader_graph[i])
			date_time=row["DATE_TIME"]
			name=row["NAME"]
			ltp=row["LTP"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
			else:
				if(k != 1):
					graph_values.append(row["DO"])
					call_time = datetime.strptime(date_time,format)
					m = call_time.minute
					s = ""
					if(m<10):
						s= "0" + str(m)
					else: 
						s = str(m)
					time_val = str(call_time.hour) + ":" + s
					time_values.append(time_val)
					k = 1
					# print(name)				
				graph_values.append(ltp)
				call_time = datetime.strptime(date_time,format)
				m = call_time.minute
				s = ""
				if(m<10):
					s= "0" + str(m)
				else: 
					s = str(m)
				time_val = str(call_time.hour) + ":" + s
				time_values.append(time_val)
			# index1 = i - 51
		readFile.close()
		st_search["graph_values"] = graph_values
		st_search["time_values"] = time_values
		return(st_search)	


def search_sensex():
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M:%S"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
			index = i - 51
		st = dict(reader[index])
		readFile.close()
	graph_values = []
	time_values = []
	k=0
	with open('new_stock_data.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader_graph = list(csv.DictReader(readFile))
		l = len(list(reader_graph))
		for i in range(0,l,51):
			row = dict(reader_graph[i])
			date_time=row["DATE_TIME"]
			name=row["NAME"]
			ltp=row["LTP"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
			else:
				if(k != 1):
					graph_values.append(row["DO"])
					call_time = datetime.strptime(date_time,format)
					m = call_time.minute
					s = ""
					if(m<10):
						s= "0" + str(m)
					else: 
						s = str(m)
					time_val = str(call_time.hour) + ":" + s
					time_values.append(time_val)
					k = 1				
				graph_values.append(ltp)
				call_time = datetime.strptime(date_time,format)
				m = call_time.minute
				s = ""
				if(m<10):
					s= "0" + str(m)
				else: 
					s = str(m)
				time_val = str(call_time.hour) + ":" + s			
				time_values.append(time_val)
			# index1 = i - 51
		readFile.close()
		st["graph_values"] = graph_values
		st["time_values"] = time_values
		return(st)

def short_term():
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
		index = i - 51
		readFile.close()

	per = []
	code = []
	inc = []
	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(index+1,index+51):
			row = dict(reader[i])
			dh=float(row["DH"])
			dl=float(row["DL"])
			pdc=float(row["PDC"])
			do=float(row["DO"])
			ltp=float(row["LTP"])
			com_name=str(row["NAME"])
			
			df=dayDiff(dh=dh,dl=dl)
			pdf=previousDayDiff(pdc=pdc,do=do)
			cdf=currentDayDiff(ltp=ltp,do=do)
			code.append(com_name)
			per.append(df+pdf+cdf) 
			inc.append((dh - ltp)/ltp)
			# print(com_name, (ltp - do)/ltp * 100,df+pdf+cdf)
			
		readFile.close()

	for i in range(len(inc)):
		for j in range(i + 1, len(inc)):

			if inc[i] > inc[j]:
				inc[i], inc[j] = inc[j], inc[i]
				code[i], code[j] = code[j], code[i]
				per[i], per[j] = per[j], per[i]

	
	for i in range(len(per)):
		print(per[i],inc[i],code[i])

	count = 0
	codes = []

	for i in range(len(per)-1, -1, -1):
		if(per[i] == 3 or per[i] == 2 or per[i] == 1 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	indices = []
	indices.append(0)
	while len(indices)!=3:
		r = random.randint(1,4)
		k = 0
		for i in range(0, len(indices)):
			if(r == indices[i]):
				k = 1
		if(k == 0):
			indices.append(r)
	print(indices)
	newcodes = []
	for i in range(3):
		j = indices[i]
		newcodes.append(codes[j])
	print(newcodes)
	print(codes)
	budget_stocks = []
	for i in range(index+1,index+51):
		row = dict(reader[i])
		com_name=str(row["NAME"])
		for j in range(3):
			if(newcodes[j] ==com_name):
				code_index = com_code.index(com_name)
				graph_values = []
				time_values = []
				k=0
				with open('new_stock_data.csv','r',newline='',encoding='utf-8-sig') as readFile:
					reader_graph = list(csv.DictReader(readFile))
					l = len(list(reader_graph))
					for i in range(code_index,l,51):
						row = dict(reader_graph[i])
						date_time=row["DATE_TIME"]
						name=row["NAME"]
						ltp=row["LTP"]
						dummydate = datetime.date(datetime.now())
						diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
						if(diff1.total_seconds() < 0):
							break
						else:
							if(k != 1):
								graph_values.append(row["DO"])
								call_time = datetime.strptime(date_time,format)
								m = call_time.minute
								s = ""
								if(m<10):
									s = "0" + str(m)
								else: 
									s = str(m)
								time_val = str(call_time.hour) + ":" + s
								time_values.append(time_val)
								k = 1
							graph_values.append(ltp)
							call_time = datetime.strptime(date_time,format)
							m = call_time.minute
							s = ""
							if(m<10):
								s= "0" + str(m)
							else: 
								s = str(m)
							time_val = str(call_time.hour) + ":" + s
							time_values.append(time_val)
					readFile.close()
					st_5 = row
					st_5["graph_values"] = graph_values
					st_5["time_values"] = time_values
				budget_stocks.append(st_5)

	return(budget_stocks)

def long_term():
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
		index = i - 51
		readFile.close()

	per = []
	code = []
	inc = []
	with open('new_stock_data_friday.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(index+1,index+51):
			row = dict(reader[i])
			dh=float(row["DH"])
			dl=float(row["DL"])
			pdc=float(row["PDC"])
			do=float(row["DO"])
			ltp=float(row["LTP"])
			com_name=str(row["NAME"])
			wh52=float(row["WH52"])
			
			code.append(com_name)
			inc.append((wh52 - ltp)/ltp)
			# print(com_name, (ltp - do)/ltp * 100,df+pdf+cdf)
			
		readFile.close()
	for i in range(len(inc)):
		for j in range(i + 1, len(inc)):
			if inc[i] > inc[j]:
				inc[i], inc[j] = inc[j], inc[i]
				code[i], code[j] = code[j], code[i]
	
	for i in range(len(inc)):
		print(inc[i],code[i])

	count = 0
	codes = []

	for i in range(len(inc)-1, -1, -1):
		if(count < 7):
			codes.append(code[i])
			count+=1
		if(count >6): 
			break
	indices = []
	indices.append(0)
	while len(indices)!=3:
		r = random.randint(1,6)
		k = 0
		for i in range(0, len(indices)):
			if(r == indices[i]):
				k = 1
		if(k == 0):
			indices.append(r)
	print(indices)
	newcodes = []
	for i in range(3):
		j = indices[i]
		newcodes.append(codes[j])
	print(newcodes)
	print(codes)
	budget_stocks = []
	for i in range(index+1,index+51):
		row = dict(reader[i])
		com_name=str(row["NAME"])
		for j in range(3):
			if(newcodes[j] ==com_name):
				code_index = com_code.index(com_name)
				graph_values = []
				time_values = []
				k=0
				with open('new_stock_data.csv','r',newline='',encoding='utf-8-sig') as readFile:
					reader_graph = list(csv.DictReader(readFile))
					l = len(list(reader_graph))
					for i in range(code_index,l,51):
						row = dict(reader_graph[i])
						date_time=row["DATE_TIME"]
						name=row["NAME"]
						ltp=row["LTP"]
						dummydate = datetime.date(datetime.now())
						diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
						if(diff1.total_seconds() < 0):
							break
						else:
							if(k != 1):
								graph_values.append(row["DO"])
								call_time = datetime.strptime(date_time,format)
								m = call_time.minute
								s = ""
								if(m<10):
									s = "0" + str(m)
								else: 
									s = str(m)
								time_val = str(call_time.hour) + ":" + s
								time_values.append(time_val)
								k = 1
							graph_values.append(ltp)
							call_time = datetime.strptime(date_time,format)
							m = call_time.minute
							s = ""
							if(m<10):
								s= "0" + str(m)
							else: 
								s = str(m)
							time_val = str(call_time.hour) + ":" + s
							time_values.append(time_val)
					readFile.close()
					st_5 = row
					st_5["graph_values"] = graph_values
					st_5["time_values"] = time_values
				budget_stocks.append(st_5)

	return(budget_stocks)

def budget_stocks(budget, ls):
	if(ls == str(0)):
		return(short_term())
	else:
		return(long_term())

@app.route('/')
def home():
    return json.dumps("Friction Hacks")
@app.route('/top5')
def top5():
    return json.dumps(top_5())

@app.route('/search')
def search():
 	search_code = request.args.get('code')
 	return json.dumps(search_stock(search_code))

@app.route('/sensex')
def sensex():
 	return json.dumps(search_sensex())

@app.route('/budget')
def budget():
	budget = request.args.get('budget')
	long_short = request.args.get('ls')
	return json.dumps(budget_stocks(budget, long_short))

if __name__ == '__main__':
    app.run(debug=True, port=3000)

