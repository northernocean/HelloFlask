from flask import Flask, render_template
from dotenv import load_dotenv
import json
import dbaccess as db
import requests
import os

# -----
# Setup
# -----

# load any additional environment variables defined in a .env file
load_dotenv()

IS_PRODUCTION_ENVIRONMENT = False

if('DATABASE_URL') in os.environ:
    # at Heroku there is a database url environment variable
    # with connection information for postgres. Otherwise,
    # assumption is we are running locally for development
    IS_PRODUCTION_ENVIRONMENT = True

if IS_PRODUCTION_ENVIRONMENT:
    API_BASE_URL = "https://hidden-stream-21468.herokuapp.com/"
else:
    API_BASE_URL = "http://localhost:5000/"

# ------------------
# Start flask server
# ------------------
app = Flask(__name__)

# ------
# Routes
# ------
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/earthquakes/postgres/1")
def earthquakes_postgres_1():
    xs, ys = db.get_earthquake_count_by_years()
    view_data = {"xs": xs, "ys": ys}
    view_data["data_source"] = db.DATA_SOURCE
    return render_template('earthquakes_postgres_1.html', view_data=view_data)

@app.route("/earthquakes/p2")
def earthquakes_p2():
    return render_template('earthquakes.html', view_data={'url': API_BASE_URL + 'api/earthquakes'})

@app.route("/earthquakes/s1")
def earthquakes_s1():
    # Calling the api as if it were an external api,
    # even though it is really in the same project.
    # Presumably this works (seems a little odd though),
    xs = []
    ys = []
    resource = "api/earthquakes"
    res = requests.get(API_BASE_URL + resource)
    if res.status_code == 200:
        dict_temp = res.json()
        xs = dict_temp["xs"]
        ys = dict_temp["ys"]
    return render_template(
        'index.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE + " (via api)"})

@app.route("/api/earthquakes")
def earthquakes():
    xs, ys = db.get_earthquake_count_by_years()
    results_dict = {"xs": xs, "ys": ys}
    return json.dumps(results_dict)

if __name__ == "__main__":
    app.run()

