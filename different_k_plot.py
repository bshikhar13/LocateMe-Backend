import numpy as np
import matplotlib.pyplot as pp

import MySQLdb
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="locateme")


Global_k = 10

def finalValue(Xn,xn):
	sigma = mt.sqrt(0.5*(pow((Xn-xn),2)))
	sigma_square =0.5 *(pow((Xn-xn),2))
	sign = lambda x: (1,-1) [x>0]
	print str(sign(Xn-xn)) + " : " + str(sigma) + " : " + str(sigma_square)
	Xf = Xn + ((sign(Xn-xn)) * sigma * 1)
	return Xf



def calculatePosition():
	cur = Con.cursor()
	cur.execute("SELECT * FROM apdata WHERE venue_id='"+ venue_id +"'")
	rv = cur.fetchall()
	AP_List = []
	for r in rv:
		AP_List.append(r[1])

	for ap in AP_List:
		Temp_list = []
		query = "SELECT * FROM rssi_data WHERE venue_id = '" + venue_id + "' AND ap_id='"+ ap +"' AND phone_mac='"+ phone_mac +"'ORDER BY id desc limit "+ str(Global_k+1) +""
		#print(query)
		cur.execute(query)
		rev = cur.fetchall()
		for r in rev:
			Temp_list.append(r[3])
		Temp_list = [int(i) for i in Temp_list]
		if len(Temp_list) == Global_k+1:
			xn = Temp_list.pop()
			R = sum(a-b for a,b in zip(Temp_list,Temp_list[1:])) / Global_k
			Xn_minus_1 = Temp_list.pop()
			print xn
			Xn = R+Xn_minus_1
			print Xn
			Xf = finalValue(Xn,xn)
			print Xf
			cur.execute("INSERT INTO temporary_for_graph_table (timestamp,raw_rssi,predicted_rssi,filtered_rssi) VALUES ('"+str(datetime.datetime.now())+"','"+ str(xn) +"','"+ str(Xn) +"','"+ str(Xf) +"')")
			cur.connection.commit()
			if xn != Xn:
				print("Yahoo : " + str(Xn))

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

	ttl = pp.title('Time vs Raw RSSI | Filtered RSSI')
	pp.text("bnm")
	pp.plot(t,raw_rssi,'r--',label="Raw RSSI")
	pp.plot(t,filtered_rssi,'g-',label='Filtered RSSI')
	#pp.plot(t,predicted_rssi,'b--',label='Predicted RSSI')

	pp.legend(loc='upper right', frameon=False)
	grd = pp.grid(True)
	pp.show()


if __name__ == "__main__":
	plotGraph()
