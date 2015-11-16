from flask import Flask
from flask import request
from flask.ext.mysqldb import MySQL
import json
from flask import send_file
from random import randint

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'locateme'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route("/")
def hello():
    return "Hello Worflflld! fuck the hell"

@app.route('/qrcode', methods=['GET'])
def qrcodeprocess():
	qr = request.args.get('qrcode')
	cur = mysql.connection.cursor()
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

@app.route('/getimage/<imageurl>', methods=['GET'])
def imagesending(imageurl):
	return send_file('static/img/venues/'+imageurl)


@app.route('/LENdata' , methods=['POST'])
def saveLENData():
	content = request.get_json(silent=True)
	print content['venue_id']
	venue_id = content['venue_id']
	phone_mac = content['phone_mac']
	ap_id = content['ap_id']
	rssi = content['rssi']
	cur = mysql.connection.cursor()
	query = "INSERT INTO rssi_data (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	print (query)
	cur.execute(query)
	mysql.connection.commit()
	return "done"

@app.route('/LENdataForSync', methods=['POST'])
def saveLENDataForSync():
	content = request.get_json(silent=True)
	print content['venue_id']
	venue_id = content['venue_id']
	phone_mac = content['phone_mac']
	ap_id = content['ap_id']
	rssi = content['rssi']
	cur = mysql.connection.cursor()
	query = "INSERT INTO rssi_data_for_sync (venue_id,ap_id,rssi,phone_mac) VALUES ('"+venue_id+"','"+ap_id+"','"+rssi+"','"+phone_mac+"')"
	print (query)
	cur.execute(query)
	mysql.connection.commit()
	return json.dumps("done")

@app.route('/GetLocation', methods=['GET'])
def getlocation():
	content = request.get_json(silent=True)
	data = {}
	data['x'] = randint(1,50)
	data['y'] = randint(1,50)
	json_data = json.dumps(data)
	return json_data

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=8080)