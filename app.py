from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "22dfba71e11ba5ddad53f547a8e789c7"

# 20 CITIES DATA
cities = [
    "Ahmedabad",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune",
    "Jaipur",
    "Surat",
    "Lucknow",
    "Kanpur",
    "Nagpur",
    "Indore",
    "Bhopal",
    "Patna",
    "Goa",
    "Udaipur",
    "New York",
    "London"
]

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    forecast = []
    error = None

    # DEFAULT CITY
    city = "Ahmedabad"

    if request.method == "POST":
        city = request.form.get("city")

    # CURRENT WEATHER API
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    weather_response = requests.get(weather_url)

    weather_data = weather_response.json()

    # FORECAST API
    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    forecast_response = requests.get(forecast_url)

    forecast_data = forecast_response.json()

    print(weather_data)

    if str(weather_data.get("cod")) != "200":

        error = weather_data.get(
            "message",
            "City not found!"
        )

    else:

        weather = {

            "city": weather_data["name"],

            "country": weather_data["sys"]["country"],

            "temp": weather_data["main"]["temp"],

            "humidity": weather_data["main"]["humidity"],

            "wind": weather_data["wind"]["speed"],

            "description": weather_data["weather"][0]["description"],

            "icon": weather_data["weather"][0]["icon"]
        }

        # 5 FORECAST CARDS
        forecast_dates = []

        for item in forecast_data["list"]:

            date = item["dt_txt"].split(" ")[0]

            # ADD ONLY UNIQUE DATES
            if date not in forecast_dates:

                forecast_dates.append(date)

                forecast.append({

                    "date": date,

                    "temp": item["main"]["temp"],

                    "icon": item["weather"][0]["icon"]

                })

            # ONLY 5 DAYS
            if len(forecast) == 5:
                break

    return render_template(

        "index.html",

        weather=weather,

        forecast=forecast,

        error=error,

        cities=cities
    )

if __name__ == "__main__":
    app.run(debug=True)