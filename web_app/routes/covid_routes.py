# web_app/routes/home_routes.py

from flask import Blueprint, render_template, request

#from app.weather_service import get_hourly_forecasts

covid_routes = Blueprint("covid_routes", __name__)

@covid_routes.route("/stateandcounty/form")
def stateandcounty_form():
    print("VISITED THE STATE AND COUNTY FORM...")
    return render_template("stateandcounty.html")

@covid_routes.route("/results", methods=["GET", "POST"])
def results():
    print("GENERATING COVID-19 COUNTY STATS...")

    if request.method == "POST":
        print("FORM DATA:", dict(request.form)) #> {'zip_code': '20057'}
        zip_code = request.form["zip_code"]
    elif request.method == "GET":
        print("URL PARAMS:", dict(request.args))
        zip_code = request.args["zip_code"]

    results = get_hourly_forecasts(zip_code)
    print(results.keys())
    return render_template("weather_forecast.html", zip_code=zip_code, results=results)