from flask import Flask, render_template, send_file , jsonify,request
import requests
import os
import psycopg2
from psycopg2 import Error
from datetime import datetime, timezone

# #For Local Testing
# app = Flask(__name__, static_url_path='')

#For Deploying
app = Flask(__name__)
last_temp = None

def connect_db():
        try:
            # Connect to an existing database
            connection = psycopg2.connect(  user="testadmin",
                                            password="testAdmin123",
                                            host="127.0.0.1",
                                            port="5432",
                                            database="test_db")

            # Create a cursor to perform database operations
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            # Fetch result
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")
            return connection
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)



def write_to_db(sensor_time,temperature):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        insert_data_query = '''INSERT INTO sensor_data(sensor_time, temperature) VALUES (%s, %s);'''
        cursor.execute(insert_data_query,(sensor_time,temperature))
        connection.commit()
        print("1 sensor data inserted successfully")   
    except (Exception, Error) as error:
        print("Error while inserting data", error)   
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")



@app.route('/')
def hello_world():
    return render_template("index.html",temperature = last_temp)



@app.route('/get_last_temp', methods= ['GET'])
def get_last_temp():
    global last_temp
    if last_temp:
        print("last temperature: {}".format(last_temp))
        return jsonify(temperature=str(last_temp)+"°C")
    else:
        print("No temperature reading")
        return jsonify(temperature="No temperature reading !")

@app.route('/get_last_records', methods= ['GET'])
def get_last_records():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id,sensor_time,temperature FROM sensor_data order by id desc limit 10;")
        last_record = cursor.fetchall()
        # print(last_record)
        return jsonify(last_record)

    except (Exception, Error) as error:
        print("Error while fetching data;", error)   
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/update-sensor',methods=['POST'])
def update_sensor():
    global last_temp
    if request.method == 'POST':        
        sensor_value = request.form['sensor1']
        if sensor_value != '-1':
            mv = (int(sensor_value) / 1024.0) * 5000
            tempc = mv / 10
            last_temp = int(tempc)
            print("Temperature: {} C".format(tempc))
            dt = str(datetime.now()).split('.',1)[0]
            write_to_db(dt,last_temp)
            return 'Temperature recorded seccessfully'
        else:
            last_temp = None
            print("no sensor reading! Nothing recorded")
            return 'no sensor reading! Nothing recorded'



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
    # app.run(debug=False)