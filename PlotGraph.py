import numpy as np
import matplotlib.pyplot as pp
from matplotlib.legend_handler import HandlerLine2D
#import pandas as pd
#from scipy import stats
#import seaborn as sns
#sns.set(color_codes=True)

import MySQLdb
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="locateme")


def plotGraph():
	raw_rssi = []
	filtered_rssi = []
	predicted_rssi = []

	Cursor = Con.cursor()
	sql = "SELECT * FROM temporary_for_graph_table"
	Cursor.execute(sql)
	rev = Cursor.fetchall()
	for i in rev:
		raw_rssi.append(i[1])
		predicted_rssi.append(i[2])
		filtered_rssi.append(i[3])
		print i[1] + " : " + i[2]
	length = len(raw_rssi)
	t = np.arange(0, length, 1)
	pp.xlabel('Time')
	pp.ylabel('RSSI Value')

	ttl = pp.title('Time vs Raw RSSI | Filtered RSSI : k = 5')
	pp.plot(t,raw_rssi,'r--',label="Raw RSSI")
	pp.plot(t,filtered_rssi,'g-',label='Filtered RSSI')
	#pp.plot(t,predicted_rssi,'b--',label='Predicted RSSI')

	pp.legend(loc='upper right', frameon=False)
	grd = pp.grid(True)
	pp.show()


if __name__ == "__main__":
	plotGraph()
