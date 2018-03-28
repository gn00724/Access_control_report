#update wicked is good17.1013

import os
import sys
from datetime import datetime
from datetime import date
import math

#DataZone
WorkerDicList = {"jasonc":"周世杰","timmy":"周宇澤","balah":"張瑞東","les":"李秉倫","gregt":"蔡佳儒","Jessik":"張瑞東","wesliec":"章逸翔","john12926":"黃冠璋","scotth":"黃韋翔","nick":"黃韋翔","wilsonyo":"何宗祐"}


startDate = ""
EndDate = ""
workerdb_class = ""
workerdb_dic = {}
counttingDay = []
normalWorkingHour = datetime.strptime("1900-01-01 08:00","%Y-%m-%d %H:%M")
m_workhour = datetime.strptime("12:30","%H:%M")
a_workhour = datetime.strptime("13:30","%H:%M")
zone_zero = datetime.strptime("00:00","%H:%M")

def writeInfile(file,*data):
	try :
		for dn in data:
			file.write(dn)
			file.write(",")
	except:
		print("Data can not write or ERROR case: " + file)
	file.write("\n")
	return ""

#1.1 get the worker's in/out gate history data Location point
print("請把你想要使用的員工出入表CSV檔案拉入Command中")
Target_txt_location_r = input()
Target_txt_location = "./_process/tmp.csv"
os.system("COPY "+Target_txt_location_r+" \"./_process/tmp.csv\"")
print("Process Begin...")

try:
	ft = open(Target_txt_location,"r")
except:
	print("請確認是否有此文件在以下位置: "  + Target_txt_location)
	print("或檔案已經處於開啟狀態")
	sys.exit()

for dr in ft.readlines():

	dr = dr.split(",")
	dataDaykey = dr[6].replace("?","").strip("\n")

	if dataDaykey in counttingDay:
		None
	elif "/" in dataDaykey:
		counttingDay.append(dataDaykey)
		counttingDay.sort()
counttingDay.sort()
startDate = counttingDay[0].replace("/","-")
EndDate = counttingDay[len(counttingDay)-1].replace("/","-")

ft.close()

try:
	ft = open(Target_txt_location,"a")
except:
	print("請確認是否有此文件在以下位置: "  + Target_txt_location)
	print("或檔案已經處於開啟狀態")
	sys.exit()

#1.2 put the SVNLOG DATA in Target_txt:
# 序號/門別/狀態/姓名/部門/卡號/日期/時間  	

#Get log

try:
	None
	os.system("svn log http://192.168.1.24/svn/tdh_game_dev/Trunk -r " + "{" +startDate + "}" + ":" + "{" + EndDate + "}" + " > ./_process/SVNLog_History.txt")
	os.system("svn log http://192.168.1.24/svn/tdh_doc/ -r " + "{" +startDate + "}" + ":" + "{" + EndDate + "}" + " > ./_process/SVNLog_History.txt")

except:
	print("Getting ERROR in Catching SVN Server")
	sys.exit()
	
	
f = open("./_process/SVNLog_History.txt","r")
fx = f.readlines()

count = 0
#Write Log in Target
for x in range(len(fx)):
	if fx[x].find("------------------------------------------------------------------------") >= 0:
		try:
			rawData = fx[x+1].split("|")
			name = rawData[1].strip(" ")
			RawDay = rawData[2].split("+")[0]
			Day = RawDay.split(" ")[1].replace("-","/")
			time = RawDay.split(" ")[2]
			try:
				workername = WorkerDicList[name]
			except:
				workername = name
			writeInfile(ft,str(count),"SVN","上傳項目",workername,"PlayStar","",Day,time)
		except:
			print("")
		count+=1

	
ft.close()
f.close()


class WorkerData:
	def __init__(self, name):
		self.name = name
		self.workerID = ""
		#{"day":[times]}
		self.dic_workerDayEnter = {}
	
ft = open(Target_txt_location,"r")

for dr in ft.readlines():

	dn = dr.split(",")

	dataName = dn[3].replace("?","").strip("\n")
	dataKey = dn[5].replace("?","").strip("\n")
	dataDay = dn[6].replace("?","").strip("\n")
	dataRawtime = dn[7].replace("?","").strip("\n")

	try:
		dataTime = datetime.strptime(dataRawtime,"%H:%M:%S")
	except:
		dataTime = ""
	
	if workerdb_dic.get(dataName) == None:
		workerdb_dic[dataName] = WorkerData(dataName)

	workerdb_dic[dataName].workerID = dataKey
	if workerdb_dic[dataName].dic_workerDayEnter.get(dataDay) == None:
		workerdb_dic[dataName].dic_workerDayEnter[dataDay] = [dataTime]
		
	else:
		workerdb_dic[dataName].dic_workerDayEnter[dataDay].append(dataTime)

	workerdb_dic[dataName].dic_workerDayEnter[dataDay].sort()

keys = workerdb_dic.keys()

ff = open("./Data/PlayStar_worker.csv","w")
count = 1
#write title
writeInfile(ff,"序號","員工","上班日期","上班時間","下班時間","工時","異常狀態","請假時間","請假假別","確認請假資訊_簽名欄","備註")
for x in keys:
	diclocate = workerdb_dic[x]
	m_date = counttingDay
	errorType = False

	for y in m_date:
		try:
			mintime = diclocate.dic_workerDayEnter[y]
		except:
			d = ""
			a = datetime.strptime(y,"%Y/%m/%d")
			weekday = date(a.year,a.month,a.day).weekday()
			c = WorkerDicList.values()
			if weekday < 5 and diclocate.name in c :
				workingStatus = "請確認是否有請假等相關紀錄"
				d_str = "需請假 全天"
				writeInfile(ff,str(count),str(diclocate.name),str(y),"","","",workingStatus,d_str)
				count+=1
			continue

		mintime = diclocate.dic_workerDayEnter[y][0]
		maxtime = diclocate.dic_workerDayEnter[y][len(diclocate.dic_workerDayEnter[y])-1]
		workingStatus = ""
		tmp_mhour = m_workhour - mintime
		tmp_ahour = maxtime - a_workhour

		if mintime > a_workhour:
			tmp_ahour = maxtime - mintime

		#print(m_workhour,mintime,tmp_mhour)
	
		if tmp_mhour.days < 0:
			tmp_mhour = zone_zero
		elif tmp_ahour.days < 0:
			tmp_ahour = zone_zero
			
		rH = tmp_mhour + tmp_ahour
		#print(tmp_mhour)
		#print(tmp_mhour,tmp_ahour,rH)
		
		try:
			workerHour = datetime.strptime(str(rH),"%Y-%m-%d %H:%M:%S")
			
		except:
			workerHour = datetime.strptime(str(rH),"%H:%M:%S")
			workerHour.replace(year=1900, month=1, day=1)
		c = normalWorkingHour - workerHour
		d_cal = round(c.total_seconds() / 3600,3)
		d_str = ""
#		if d_cal > 0:
#			d_str = "需請假 " + str(round(d_cal,1)) + " 小時"
#			print(d_cal)
#		elif d_cal == 9.0:
#			d_str = ""

		try:
			if workerHour.hour <= 7 and workerHour.weekday < 5:
				if workerHour.minute >= 30 and workerHour.hour == 7:
					None
				else:
					workingStatus = "工時未滿8小時"
					d_str = "需請假 " + str(round(d_cal,1)) + " 小時"
			if mintime.hour >= 14:
				workingStatus = "請確認上班是否打卡"
			if maxtime.hour <= 17:
				workingStatus = "請確認下班是否打卡"
				
			if diclocate.name in WorkerDicList.values():
				writeInfile(ff,str(count),str(diclocate.name),str(y),str(mintime.strftime("%H:%M:%S")),str(maxtime.strftime("%H:%M:%S")),str(workerHour.strftime("%H:%M")),workingStatus,d_str)
				count+=1
		except:
			None

print("Please type any keys")
input()