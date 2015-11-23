import numpy as np
import matplotlib.pyplot as pp
from matplotlib.legend_handler import HandlerLine2D

import MySQLdb
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="len")

def insert(a,b,c,x,y):
	Cursor = Con.cursor()
	#print "y"
	Cursor.execute("INSERT INTO finalNNData (x1,x2,x3,y1,y2) VALUES ('"+str(a)+"','"+ str(b) +"','"+ str(c) +"','"+ str(x) +"','" +str(y) + "')")
	Cursor.connection.commit()			


def util():
	raw_rssi = []
	Cursor = Con.cursor()
	#sql = "SELECT * FROM rssi_data_collect WHERE `ssid0` = 'LOCATEME-SS3'"
	x = 5
	y = 5
	for num in range(y,24):
		sql = "SELECT * FROM rssi_data_collect WHERE x='"+str(x)+"' AND y='"+str(num)+"'"
		Cursor.execute(sql)
		rev = Cursor.fetchall()
		a = []
		b = []
		c = []
		for i in rev:
			if i[0] == 'LOCATEME-SS1':
				a.append(i[1])
			if i[0] == 'LOCATEME-SS2':
				b.append(i[1])
			if i[0] == 'LOCATEME-SS3':
				c.append(i[1])
		for a1 in a:
			for b1 in b:
				for c1 in c:
					insert(a1,b1,c1,x,num)
			
if __name__ == "__main__":
	util()
