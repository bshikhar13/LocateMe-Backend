import numpy as np
import matplotlib.pyplot as pp
from matplotlib.legend_handler import HandlerLine2D
#import pandas as pd
#from scipy import stats
#import seaborn as sns
#sns.set(color_codes=True)

import MySQLdb
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="len")


def plotGraph():
	raw_rssi = []
	Cursor = Con.cursor()
	#sql = "SELECT * FROM rssi_data_collect WHERE `ssid0` = 'LOCATEME-SS3'"
	sql = "SELECT * FROM rssi_data_collect"
	Cursor.execute(sql)
	rev = Cursor.fetchall()
	for i in rev:
		if i[0] == 'LOCATEME-SS1':
			raw_rssi.append(i[1])
		
	length = len(raw_rssi)
	t = np.arange(0, length, 1)
	pp.xlabel('Time')
	pp.ylabel('RSSI Value')

	ttl = pp.title('LOCATEME-SS3')
	pp.plot(t,raw_rssi,'r--',label="Raw RSSI")
	#pp.plot(t,predicted_rssi,'b--',label='Predicted RSSI')

	pp.legend(loc='upper right', frameon=False)
	grd = pp.grid(True)
	pp.show()


if __name__ == "__main__":
	plotGraph()
