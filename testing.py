import MySQLdb
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="locateme")
Cursor = Con.cursor()
sql = "SELECT * FROM apdata"
Cursor.execute(sql)

