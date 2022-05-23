from flask import abort, Flask, request, render_template
import requests
from time import strftime , gmtime
from datetime import datetime , time
# ================== # Info # ================== #

app = Flask(__name__, static_folder="static")
API_KEY = ""

# ================== # Get Weather # ================== #
def get_weather(city):
    api=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    json_data=requests.get(api).json()
    if json_data['cod'] in [404,"404"]:
        return 
    condition=json_data['weather'][0]['main']
    temp=int(json_data['main']['temp'] - 273.15)
    min_temp=int(json_data['main']['temp_min'] - 273.15)
    max_temp=int(json_data['main']['temp_max'] - 273.15)
    pressure=json_data['main']['pressure']
    humidity=json_data['main']['humidity']
    wind=json_data['wind']['speed']
    sunrise=strftime("%I:%M:%S" , gmtime(json_data['sys']['sunrise'] - 21600))
    sunset=strftime("%I:%M:%S" , gmtime(json_data['sys']['sunset'] - 21600))

    return condition,str(temp)+"ْ C", str(max_temp),str(min_temp),str(pressure),str(humidity),str(wind),str(sunrise),str(sunset)

# ================== # Home # ================== #


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

# ================== # Weather # ================== #
@app.route("/search/", methods=['GET'])
def weather():
    if not request.args:
        abort(404)
    info = get_weather(request.args["city"])
    if not info:
        abort(404)

    now = datetime.now()
    now_time = now.time()
    status = ""
    if now_time >= time(23,00) or now_time <= time(8,00):
        status = "night"
    else:
        status = "day"

    context = {
        "status":status,
        "city":request.args["city"],
        "stat":info[0],
        "statS":info[1],
        "Sunrise":info[7],
        "Sunset":info[8],
    }
    print(context)
    return render_template("weather.html",**context)

# ================== # Run # ================== #
if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)
