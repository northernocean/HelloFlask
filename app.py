from flask import Flask, render_template
from dotenv import load_dotenv
import json
import dbaccess as db
import requests
import os

load_dotenv()
app = Flask(__name__)

if('DATABASE_URL') in os.environ:
    API_BASE_URL = "https://hidden-stream-21468.herokuapp.com/"
else:
    API_BASE_URL = "http://localhost:5000/"

@app.route("/")
def index():
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

@app.route("/earthquakes")
def earthquakes_view():
    return render_template('earthquakes.html', view_data={'url': API_BASE_URL + 'api/earthquakes'})

@app.route("/api/earthquakes")
def earthquakes():
    xs, ys = db.get_earthquake_count_by_years()
    results_dict = {"xs": xs, "ys": ys}
    return json.dumps(results_dict)

if __name__ == "__main__":
    app.run()

