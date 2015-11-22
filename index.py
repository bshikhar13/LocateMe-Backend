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
import redis
import numpy                                             
from numpy import sqrt, dot, cross                       
from numpy.linalg import norm 
from itertools import imap

#MySQL and Redis Instances
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="locateme")

app = Flask(__name__)

Global_k = 2

def intersecting_points(P1,P2,R1,R2):
	e = P2[0] - P1[0]
	f = P2[1] - P1[1]
	p = mt.sqrt(mt.pow(e,2)+mt.pow(f,2))
	k = ((mt.pow(p,2) + mt.pow(R1,2) - mt.pow(R2,2)) / (2*p))

	x1 = P1[0] + ((e*k) / p) + ((f/p)*(mt.sqrt(abs(mt.pow(R1,2) - mt.pow(k,2)))))
	y1 = P1[1] + ((f*k) / p) - ((e/p)*(mt.sqrt(abs(mt.pow(R1,2) - mt.pow(k,2)))))
	
	x2 = P1[0] + ((e*k) / p) - ((f/p)*(mt.sqrt(abs(mt.pow(R1,2) - mt.pow(k,2)))))
	y2 = P1[1] + ((f*k) / p) + ((e/p)*(mt.sqrt(abs(mt.pow(R1,2) - mt.pow(k,2)))))
	
	Point1 = [x1,y1]
	Point2 = [x2,y2]
	return Point1,Point2


def InternalPoint(Point1,Point2,P,r):
	temp = mt.sqrt(mt.pow((Point1[0] - P[0]),2) + mt.pow((Point1[1] - P[1]),2))
	if temp < r:
		return Point1
	else:
		return Point2

def CentroidTriangle(P1,P2,P3):
	a = (P1[0] + P2[0] + P3[0])/3
	b = (P1[1] + P2[1] + P3[1])/3
	result = [a,b]
	return result

def trilaterate_area(P1,P2,P3,r1,r2,r3):
	Point1,Point2 = intersecting_points(P1,P2,r1,r2)
	internal_point1 = InternalPoint(Point1,Point2,P3,r3)
	Point3,Point4 = intersecting_points(P2,P3,r2,r3)
	internal_point2 = InternalPoint(Point3,Point4,P1,r1)
	Point5,Point6 = intersecting_points(P1,P3,r1,r3)
	internal_point3 = InternalPoint(Point5,Point6,P2,r2)
	centroid = CentroidTriangle(internal_point1,internal_point2,internal_point3)
	return centroid[0], centroid[1]


# Find the intersection of three spheres                 
# P1,P2,P3 are the centers, r1,r2,r3 are the radii       
# Implementaton based on Wikipedia Trilateration article.                              
def trilaterate(P1,P2,P3,r1,r2,r3):                      
    temp1 = list(imap(lambda m, n: m-n, P2, P1))
    e_x = temp1/norm(temp1)
    temp2 = list(imap(lambda m, n: m-n, P3, P1))
    i = dot(e_x,temp2)
    temp3 = temp2 - i*e_x
    e_y = temp3/norm(temp3)
    e_z = cross(e_x,e_y)
    temp_shikhar = list(imap(lambda m,n : m-n , P2,P1))
    d = norm(temp_shikhar)
    j = dot(e_y,temp2)
    x = (r1*r1 - r2*r2 + d*d) / (2*d)
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)
    temp4 = r1*r1 - x*x - y*y
    if temp4<0:
    	shikhar,bansal = trilaterate_area(P1,P2,P3,r1,r2,r3)
        return shikhar,bansal
    z = sqrt(temp4)
    p_12_a = P1 + x*e_x + y*e_y + z*e_z
    p_12_b = P1 + x*e_x + y*e_y - z*e_z
    shikhar,bansal = trilaterate_area(P1,P2,P3,r1,r2,r3)
    return shikhar,bansal


def finalValue(Xn,xn):
	sigma = mt.sqrt(0.5*(pow((Xn-xn),2)))
	sigma_square =0.5 *(pow((Xn-xn),2))
	sign = lambda x: (1,-1) [x>0]
	#print str(sign(Xn-xn)) + " : " + str(sigma) + " : " + str(sigma_square)
	Xf = Xn + ((sign(Xn-xn)) * sigma * 1)
	return Xf

def calculateDistance(RSSI,A,n):
	return mt.pow(10,((A-RSSI) / (10 * n)))

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
	for apdata in rv:
		Xf = 0
		ap = apdata[1]
		AP_List.append(ap)
		ap_A = apdata[2]
		ap_n = apdata[3]
		ap_X = apdata[4]
		ap_Y = apdata[5]
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
			#print xn
			Xn = R+Xn_minus_1
			#print Xn
			Xf = finalValue(Xn,xn)
			#print Xf
			cur.execute("INSERT INTO temporary_for_graph_table (timestamp,raw_rssi,predicted_rssi,filtered_rssi) VALUES ('"+str(datetime.datetime.now())+"','"+ str(xn) +"','"+ str(Xn) +"','"+ str(Xf) +"')")
			cur.connection.commit()
		
		d = calculateDistance(Xf,ap_A,ap_n)
		
		key = str(venue_id) + "_" + str(ap) + "_" + str(phone_mac) + "_" + "D"

		value = d
		#print key
		#print value
		redis_instance.set(key,value)
		
		key = str(venue_id) + "_" + str(ap) + "_" + str(phone_mac) + "_" + "X"
		value = ap_X
		redis_instance.set(key,value)

		key = str(venue_id) + "_" + str(ap) + "_" + str(phone_mac) + "_" + "Y"
		value = ap_Y
		redis_instance.set(key,value)

	P1 = [int(redis_instance.get(str(venue_id) + "_" + str(AP_List[0]) + "_" + str(phone_mac) + "_X")) , int(redis_instance.get(str(venue_id) + "_" + str(AP_List[0]) + "_" + str(phone_mac) + "_Y")) , 0]
	P2 = [int(redis_instance.get(str(venue_id) + "_" + str(AP_List[1]) + "_" + str(phone_mac) + "_X")) , int(redis_instance.get(str(venue_id) + "_" + str(AP_List[1]) + "_" + str(phone_mac) + "_Y")) , 0]
	P3 = [int(redis_instance.get(str(venue_id) + "_" + str(AP_List[2]) + "_" + str(phone_mac) + "_X")) , int(redis_instance.get(str(venue_id) + "_" + str(AP_List[2]) + "_" + str(phone_mac) + "_Y")) , 0]
	#print P1
	#print P2
	#print P3
	R1 = float(redis_instance.get(str(venue_id) + "_" + str(AP_List[0]) + "_" + str(phone_mac) + "_D"))
	R2 = float(redis_instance.get(str(venue_id) + "_" + str(AP_List[1]) + "_" + str(phone_mac) + "_D"))
	R3 = float(redis_instance.get(str(venue_id) + "_" + str(AP_List[2]) + "_" + str(phone_mac) + "_D"))

	print "Radius 1 : " + str(R1)
	print "Radius 2 : " + str(R2)
	print "Radius 3 : " + str(R3)
	result_x,result_y = trilaterate(P1,P2,P3,R1,R2,R3)
	print "Finale X : " + str(result_x)
	print "Finale Y : " + str(result_y)
	print type(result_x)
	print type(result_y)
	pixelX = (int(result_x) * 40 ) + 20
	pixelY = (int(result_y) * 40 ) + 20
	return pixelX, pixelY

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
	data['image_url'] = rv[0][4]
	data['description'] = rv[0][5]
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
	#print content['venue_id']
	venue_id = content['venue_id']
	phone_mac = content['phone_mac']
	ap_id = content['ap_id']
	rssi = content['rssi']
	cur = Con.cursor()
	#query = "INSERT INTO rssi_data_for_sync (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	query = "INSERT INTO rssi_data (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	#print (query)
	cur.execute(query)
	cur.connection.commit()
	return json.dumps("done")

@app.route('/GetLocation', methods=['POST'])
def getlocation():
	content = request.get_json(silent=True)
	venue_id =  content['venue_id']
	phone_mac = content['phone_mac']
	data = {}
	data['x'], data['y'] = calculatePosition(venue_id,phone_mac)
	#data['x'] = randint(100,500)
	#data['y'] = randint(100,500)
	json_data = json.dumps(data)
	return json_data


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=8080)