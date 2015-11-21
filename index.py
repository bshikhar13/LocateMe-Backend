from flask import Flask
from flask import request
import os
#from flask.ext.mysqldb import MySQL
import json
from flask import send_file
from random import randint
import datetime
import MySQLdb
import numpy as np
import math as mt
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="locateme")

app = Flask(__name__)
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'locateme'
# app.config['MYSQL_HOST'] = 'localhost'
#mysql = MySQL(app)

Global_k = 5

def finalValue(Xn,xn):
	sigma = mt.sqrt(0.5*(pow((Xn-xn),2)))
	sigma_square =0.5 *(pow((Xn-xn),2))
	sign = lambda x: (1,-1) [x>0]
	print str(sign(Xn-xn)) + " : " + str(sigma) + " : " + str(sigma_square)
	Xf = Xn + ((sign(Xn-xn)) * sigma * 1)
	return Xf

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def calculatePosition(venue_id,phone_mac):
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
@app.route("/")
def hello():
    return "Hello Worflflld! fuck the hell"

@app.route('/qrcode', methods=['GET'])
def qrcodeprocess():
	qr = request.args.get('qrcode')
	cur = Con.cursor()
	cur.execute("SELECT * FROM venuedata WHERE id='" + qr + "'")
	rv = cur.fetchall()
	data = {}
	data['venue_id'] = rv[0][0]
	data['ap1'] = rv[0][1]
	data['ap2'] = rv[0][2]
	data['ap3'] = rv[0][3]
	data['ap4'] = rv[0][4]
	data['image_url'] = rv[0][5]
	data['description'] = rv[0][6]
	json_data = json.dumps(data)
	return json_data

@app.route('/getimage/<mapid>', methods=['GET'])
def imagesending(mapid):
	return send_file('C:/xampp/htdocs/LEN-Admin/static/img/venues/'+mapid)


@app.route('/LENdata' , methods=['POST'])
def saveLENData():
	content = request.get_json(silent=True)
	#print content['venue_id']
	venue_id = content['venue_id']
	phone_mac = content['phone_mac']
	ap_id = content['ap_id']
	rssi = content['rssi']
	cur = Con.cursor()
	query = "INSERT INTO rssi_data (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	#print (query)
	cur.execute(query)
	cur.connection.commit()
	return "done"

@app.route('/LENdataForSync', methods=['POST'])
def saveLENDataForSync():
	content = request.get_json(silent=True)
	print content['venue_id']
	venue_id = content['venue_id']
	phone_mac = content['phone_mac']
	ap_id = content['ap_id']
	rssi = content['rssi']
	cur = Con.cursor()
	#query = "INSERT INTO rssi_data_for_sync (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	query = "INSERT INTO rssi_data (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	print (query)
	cur.execute(query)
	cur.connection.commit()
	return json.dumps("done")

@app.route('/GetLocation', methods=['POST'])
def getlocation():
	content = request.get_json(silent=True)
	venue_id =  content['venue_id']
	phone_mac = content['phone_mac']
	calculatePosition(venue_id,phone_mac)
	data = {}
	data['x'] = randint(100,500)
	data['y'] = randint(100,500)
	json_data = json.dumps(data)
	return json_data


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=8080)