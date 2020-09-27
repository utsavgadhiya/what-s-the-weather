# all flask imports
from flask import Flask,render_template,request,abort

# import json to load json data to python dictionary
import json

# urllib.request to make a request to api
import urllib.request

# import os
from os import environ

# define app
app = Flask(__name__)

def to_celcius(temp):
    return str(round(float(temp) - 273.16,2))

@app.route('/',methods=['POST','GET'])
def weather():
    api_key = environ.get('OPEN_WEATHER_API_KEY')
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name Mumbai
        city = 'Mumbai'

    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except ConnectionError as e:
        print('There was an error connecting to OpenWeather API. Please try again later.')
        print(e)
        return abort(500)

    # converting json data to dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']),
        "temp_cel": to_celcius(list_of_data['main']['temp']),
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "cityname":str(city),
    }
    return render_template('home.html',data=data)

#  __main__
if __name__ == '__main__':
    app.run(debug=False)
