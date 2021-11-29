from flask import Flask, render_template
from dotenv import load_dotenv
import json
import dbaccess as db
import requests

load_dotenv()
app = Flask(__name__)

api_url = "https://hidden-stream-21468.herokuapp.com/"

@app.route("/")
def index():
    # Calling the api as if it were an external api,
    # even though it is really in the same project.
    # Presumably this works (seems a little odd though),
    xs = []
    ys = []
    resource = "api/earthquakes"
    res = requests.get(api_url + resource)
    if res.status_code == 200:
        dict_temp = res.json()
        xs = dict_temp["xs"]
        ys = dict_temp["ys"]
    return render_template(
        'index.html',
        data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE + " (via api)"})


@app.route("/api/earthquakes")
def earthquakes():
    xs, ys = db.get_earthquake_count_by_years()
    results_dict = {"xs": xs, "ys": ys}
    return json.dumps(results_dict)

if __name__ == "__main__":
    app.run()

