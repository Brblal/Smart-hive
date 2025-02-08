import os
from flask import Flask, render_template
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import db
from db import average_temperature

app = Flask(__name__)
current_temp = ""
current_weight = ""

# Konfigurace AWS IoT klienta
myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint("a3js4n5qgv7sx4-ats.iot.eu-north-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./rootCA.pem", './b0138100d39afeea8f7451ae671d1557e775148e3eb72829151cd462121967f5-private.pem.key', './b0138100d39afeea8f7451ae671d1557e775148e3eb72829151cd462121967f5-certificate.pem.crt')

# Callback funkce pro zpracování přijatých zpráv
import json

def customCallback(client, userdata, message):
    print("Received a new message: ")
    payload = message.payload.decode()
    print(payload)  
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    global current_temp, current_weight

    try:
        # Pokus o parsování JSON zprávy
        data = json.loads(payload)  # Načtení JSON dat do slovníku

        if "temperature" in data:
            process_temperature(data["temperature"])
        if "weight" in data:
            process_weight(data["weight"])
        if "humidity" in data:
            print("Humidity:", data["humidity"])  # Můžeš přidat zpracování vlhkosti
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON. Raw message:", payload)
    except Exception as e:
        print("Error processing message:", e)

def process_temperature(temperature_value):
    global current_temp
    current_temp = str(temperature_value)  # Převedení na string
    print("Received temperature:", current_temp)
    db.save_temperature_to_db(current_temp)

def process_weight(weight_value):
    global current_weight
    current_weight = str(weight_value)  # Převedení na string
    print("Received weight:", current_weight)
    db.save_weight_to_db(current_weight)

# Funkce pro připojení a přihlášení k AWS IoT
def connect_and_subscribe():
    try:
        myMQTTClient.connect()
        myMQTTClient.subscribe("device/data", 1, customCallback)  # Změňte "topic" podle vašeho nastavení
        print("Connected and subscribed to AWS IoT")
    except Exception as e:
        print("Error connecting or subscribing to AWS IoT:", e)

# Inicializace Flask aplikace
@app.route('/')
def index():
    data_from_db = db.get_temperature_data()
    kg_from_db = db.get_weight_data()
    
    current_temp = db.get_latest_temperature()
    current_weight = db.get_latest_weight()
    average = average_temperature()
    
    return render_template('index.html', data=data_from_db, current_temp=current_temp, avg_temp=average, kg=kg_from_db, current_weight=current_weight)
@app.route('/temp')
def temp():
    data_from_db = db.get_temperature_data()
    kg_from_db = db.get_weight_data()
    
    average = average_temperature()
    return render_template('temp.html', data=data_from_db, current_temp=current_temp, avg_temp=average, kg=kg_from_db, current_weight=current_weight)
@app.route("/login")
def login():
    return render_template("login.html")

# Spojení a přihlášení k AWS IoT při spuštění aplikace
if __name__ == '__main__':
    db.init_db()  # Inicializace databáze při spuštění aplikace
    connect_and_subscribe()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))