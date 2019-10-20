import csv
with open('stock_data_friday1.csv','w',newline='',encoding='utf-8-sig') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerow(['NAME','LTP','DC','DO','DH','DL','PDC','CH','PCH','DV','LTT','WH52','WL52','DATE_TIME','DATE_TODAY','HOUR','MIN'])
		writeFile.close()

with open('stock_data.csv','r',newline='',encoding='utf-8-sig') as writeFile:
	reader = csv.DictReader(writeFile)
	
	for row in reader:
		com_name=str(row["NAME"])
		ltp=row["LTP"].replace(',','')
		dc=row["DC"].replace(',','')
		do=row["DO"].replace(',','')
		dh=row["DH"].replace(',','')
		dl=row["DL"].replace(',','')
		pdc=row["PDC"].replace(',','')
		ch=row["CH"].replace(',','')
		pch=row["PCH"].replace(',','')
		dv=row["DV"].replace(',','')
		ltt=row["LTT"]
		wh52=row["WH52"].replace(',','')
		wl52=row["WL52"].replace(',','')
		date_time=row["DATE_TIME"]
		date_today=row["DATE_TODAY"]
		hour=row["HOUR"]
		min=row["MIN"]
		with open('new_srock_datail1.csv','a',newline='',encoding='utf-8-sig') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerow([com_name,ltp,dc,do,dh,dl,pdc,ch,pch,dv,ltt,wh52,wl52,date_time,date_today,hour,min])
			writeFile.close()	 
		writeFile.close()
