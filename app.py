import config
from boto3 import session
from dotenv import load_dotenv
import flask
import requests
import configparser
import boto3
import os
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

load_dotenv()
#def get_api_key():
#    config = configparser.ConfigParser()
#    config.read('config.ini')
#    return config['openweathermap']['api']


def get_weather_results(city_name, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}".format(city_name,api_key)
    r = requests.get(api_url)
    return r.json()

def put_visitor(Date_Time, Paris_Weather, TelAviv_Weather, NewYork_Weather, Browser, IP_Address, dynamodb=None):
    if not dynamodb:
        #config = configparser.ConfigParser()
        #config.read('config.py')
        accessid = os.getenv('aws_access_key_id')
        accessid = config.aws_access_key_id
        print('accessid')
        secretid = os.getenv('aws_secret_access_key')
        secretid = config.aws_secret_access_key
        #accessid = config['openweathermap']['aws_access_key_id']
        #secretid = config['openweathermap']['aws_secret_access_key']
        session = boto3.Session(aws_access_key_id = accessid, aws_secret_access_key = secretid)
        dynamodb = session.resource('dynamodb', region_name='us-east-2')

    table = dynamodb.Table('Visitors')
    response = table.put_item(
       Item={
            'Date_Time': Date_Time,
            'Paris_Weather': Paris_Weather,
            'TelAviv_Weather': TelAviv_Weather,
            'NewYork_Weather': NewYork_Weather,
            'Browser': Browser,
            'IP_Address': IP_Address
        }
    )
    return response

@app.route('/')


def home():
    city_name1 = "Paris"
    api_key = os.getenv('api')
    #api_key = config.api
    #api_key = get_api_key()
    data1 = get_weather_results(city_name1, api_key)
    temp1 = "{0:.2f}".format(data1["main"]["temp"])
    weather1 = data1["weather"][0]["main"]
           
    city_name2 = "Tel Aviv"
    data2 = get_weather_results(city_name2, api_key)
    temp2 = "{0:.2f}".format(data2["main"]["temp"])
    weather2 = data2["weather"][0]["main"]
    
    city_name3 = "New York"
    data3 = get_weather_results(city_name3, api_key)
    temp3 = "{0:.2f}".format(data3["main"]["temp"])
    weather3 = data3["weather"][0]["main"]

    user_agent = request.user_agent.browser
    ip_address = flask.request.remote_addr

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   
    weather_resp = put_visitor(dt_string, temp1, temp2, temp3, user_agent, ip_address)
    return render_template('home.html', location1=city_name1, temp1=temp1, weather1=weather1, location2=city_name2, temp2=temp2, weather2=weather2, location3=city_name3, temp3=temp3, weather3=weather3)

  
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000)




