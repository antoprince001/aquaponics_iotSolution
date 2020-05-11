from flask import Flask, render_template
import conf
from boltiot import Bolt
import json, time,requests



app = Flask(__name__)

class basic:
    def __init__(self):
        self.loginstatus=0
        self.username=''


@app.route("/")
@app.route("/home")
def home():
    return render_template('login.html')

@app.route("/login")
def login():
    return render_template('enter.html')

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html') 

   
@app.route('/temperature')
@app.route('/dashboard/temperature')
def temp():
 mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
 response = mybolt.analogRead('A0') 
 data = json.loads(response) 

 

 seconds=time.time()
 date=time.localtime(seconds)

 if(date.tm_mon==1):
    mon='January'
 if(date.tm_mon==2):
    mon='February'
 if(date.tm_mon==3):
    mon='March'
 if(date.tm_mon==4):
    mon='April'
 if(date.tm_mon==5):
    mon='May'
 if(date.tm_mon==6):
    mon='June'
 if(date.tm_mon==7):
    mon='July'
 if(date.tm_mon==8):
     mon='August'
 if(date.tm_mon==9):
     mon='September'
 if(date.tm_mon==10):
     mon='October'
 if(date.tm_mon==11):
     mon='November'
 if(date.tm_mon==12):
     mon='December'

 hour=int(date.tm_hour)
 hourtime=str(hour)
 if(date.tm_hour>12):
     hour=int(date.tm_hour)-12
     hourtime=str(hour)
     zone='PM'
 else:
     zone='AM'
 api_key = "df6d7566e1ff99c3e1f91ec11f22d5e9"
 base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
# Give city name 
 city_name = 'chennai'
  
# complete_url variable to store 
# complete url address 
 complete_url = base_url + "appid=" + api_key + "&q=" + city_name
  
# get method of requests module 
# return response object 
 response = requests.get(complete_url) 
  
# json method of response object  
# convert json format data into 
# python format data 
 x = response.json() 
  
# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
 if x["cod"] != "404": 
  
    # store the value of "main" 
    # key in variable y 
    y = x["main"] 
  
    # store the value corresponding 
    # to the "temp" key of y 
    current_temperature = y["temp"] 
  
    # store the value corresponding 
    # to the "pressure" key of y 
    current_pressure = y["pressure"] 
  
    # store the value corresponding 
    # to the "humidity" key of y 
    current_humidiy = y["humidity"] 
    #speed=x["wind.speed"]
  
    # store the value of "weather" 
    # key in variable z 
    z = x["weather"] 
    
    # store the value corresponding  
    # to the "description" key at  
    # the 0th index of z 
    weather_description = z[0]["description"] 
    sensor_value=data['value']
    if sensor_value!='Device is offline':
      sensor_value = int(data['value'])
      celsius=(100*sensor_value)/1024 
      fahreheit= celsius*1.8 +32
    else:
      celsius=current_temperature
      fahreheit= current_temperature
      sensor_value=current_temperature
   
    post={
     'hour': hourtime  ,
     'second': date.tm_sec,
     'minute': date.tm_min,
     'month': mon,
     'day': date.tm_mday,
     'year': date.tm_year,
     'kelvin': str(sensor_value),
     'celsius': str(celsius),
     'fahrenheit': str(fahreheit),
     'zone': zone,
     'pressure':current_pressure,
     'humidity':current_humidiy,
     'weather':z,
    
     'description':weather_description


  }
 return  render_template('temp.html', posts=post)
    #time.sleep(10)
        

if __name__ == '__main__':
    app.run(debug=True)