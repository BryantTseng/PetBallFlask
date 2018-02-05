from flask import Flask, render_template, request, jsonify
import sys
import pymysql

app=Flask(__name__)
db_data = {
    "user" : "android",
    "password" : "1234",
    "url" : "192.168.3.113",
    "dbname" : "roomii",
    "table_account" : "account",
    "roomii_account" : "roomii"
}
@app.route("/")
def hell0():
    return 'hello'
@app.route("/login")
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    db = pymysql.connect(db_data.get("url"), db_data.get("user"), db_data.get("password"), db_data.get("dbname"))
    cursor = db.cursor()
    sql='SELECT * FROM %s.account WHERE %s.account.email = "%s" and %s.account.password = "%s"'%(db_data.get("dbname"), db_data.get("dbname"), email, db_data.get("dbname"), password)
    try:
        cursor.execute(sql)
        print("try to login with email: " + email+ ", password: "+password)
        acc_result = cursor.fetchall()
        
    except:
        print('Error: '+sql)
    if(len(acc_result)==0):#not in table
        print("not in table")
        return "error with email or password"
    else:#in the table
        print(acc_result)
        sql='SELECT * FROM %s.roomii WHERE %s.roomii.roomii_ID = %s'%(db_data.get("dbname"), db_data.get("dbname"), acc_result[0][4])
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            print("try to fiind roomii ip with login data")
            roomii_result=cursor.fetchall()
            db.close()
        except:
            print("Error: "+sql)
        if(len(roomii_result)==0):
            print("no connected roomi, please setup")
        else:
            print("find roomii!")
    return jsonify(name=acc_result[0][2],email=acc_result[0][1],roomii_ip=roomii_result[0][2])
    
        #return "login success"
    return "done with error"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
