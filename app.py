from flask import Flask, render_template
from dotenv import load_dotenv
import json
import requests
import os
import data_access.data_access_postgres as db_postgres
import data_access.data_access_sqlite as db_sqlite
import data_access.data_access_mongodb as db_mongodb
import data_access.data_access_csv_local as db_csv_local
import data_access.data_access_csv_remote as db_csv_remote
import data_access.data_access_json_local as db_json_local
import data_access.data_access_json_remote as db_json_remote

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

# -----------
# Page Routes
# -----------
@app.route("/")
def index():
    return render_template('index.html', 
        route_summaries_dict=route_summaries())

@app.route("/earthquakes/postgres/1")
def earthquakes_postgres_1():
    db = db_postgres
    xs, ys = db.get_earthquake_count_by_years()
    view_data = {"xs": xs, "ys": ys, "data_source": db.DATA_SOURCE}
    return render_template('earthquakes.html', view_data=view_data)

@app.route("/earthquakes/postgres/2")
def earthquakes_postgres_2():
    # Calling the api as if it were an external api,
    # even though it is really in the same project.
    # by default the internal api uses postgres but in
    # principle the api can use any datasource with
    # the same strategies applied here for other routes.
    xs = []
    ys = []
    resource = "api/earthquakes"
    res = requests.get(API_BASE_URL + resource)
    if res.status_code == 200:
        dict_temp = res.json()
        xs = dict_temp["xs"]
        ys = dict_temp["ys"]
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': 'internal api'})

@app.route("/earthquakes/mongodb/1")
def earthquakes_mongodb_1():
    if IS_PRODUCTION_ENVIRONMENT:
        return
    db = db_mongodb
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})

@app.route("/earthquakes/sqlite/1")
def earthquakes_sqlite_1():
    db = db_sqlite
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})

@app.route("/earthquakes/csv/1")
def earthquakes_csv_1():
    db = db_csv_local
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})

@app.route("/earthquakes/csv/2")
def earthquakes_csv_2():
    db = db_csv_remote
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})

@app.route("/earthquakes/csv/3")
def earthquakes_csv_3():
    return render_template(
        'earthquakesFetchWithD3.html',
        view_data={'uri': db_csv_remote.uri,
         'data_source': 'csv-fetch'})

@app.route("/earthquakes/json/1")
def earthquakes_json_1():
    db = db_json_local
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})

@app.route("/earthquakes/json/2")
def earthquakes_json_2():
    db = db_json_remote
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'earthquakes.html',
        view_data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})

@app.route("/earthquakes/json/3")
def earthquakes_json_3():
    return render_template(
        'earthquakesFetchWithD3.html',
        view_data={'uri': db_json_remote.uri,
         'data_source': 'json-fetch'})

@app.route("/earthquakes")
def earthquakes():
    db = db_postgres
    xs, ys = db.get_earthquake_count_by_years()
    view_data = {"xs": xs, "ys": ys, "data_source": db.DATA_SOURCE}
    return render_template('earthquakes.html', view_data=view_data)

# ----------
# API Routes
# ----------
@app.route("/api/earthquakes")
def api_earthquakes():
    xs, ys = db_postgres.get_earthquake_count_by_years()
    results_dict = {"xs": xs, "ys": ys}
    return json.dumps(results_dict)

# -----
# Other
# -----
def route_summaries():
    return {
        'postgres':
        {   
            'url':'earthquakes/postgres/1',
            'description': ('Route with a postgres database data source. '
            'In this example, if the project runs locally, a '
            'connection is created to a local postgres server, '
            'and if the project is deployed to heroku, a '
            'connection is opened to a heroku-hosted postgres server.')
        },
        'postgres / api':
        {
            'url': 'earthquakes/postgres/2',
            'description': ('Route with a postgres database datasource, '
            'but routed via an api route served from the same project. '
            'Note that if you already have the database accessible in '
            'the same project you do not really an api to access the data. '
            'This setup might be useful if you intend to later move '
            'the database out of the project')
        },
        'mongodb':
        {
            'url':'earthquakes/mongodb/1',
            'description': ('Route using a mongodb data source. In this project, '
            'we have setup a local (development) mongodb datasource. '
            'This link will not work in production - the main reason is that '
            'our cloud mongodb deployment whitelists access by IP address '
            'but at heroku we do not have a static IP address and obtaining one '
            'involves a credit card and (potentially) billing charges. '
            'However, our development setup does allow use of either a local '
            'mongo server or a cloud mongo server, and plenty of other options are also available.')
        },
        'sqlite':
        {
            'url':'earthquakes/sqlite/1',
            'description': ('Route with a local sqlite (readonly) database. '
            'Per Heroku docs, sqlite is not recommended for heroku deployments. '
            'However, I have not had any issues with sqlite when used as a '
            'a read-only datasource.')
        },
        'csv / local':
        {
            'url':'earthquakes/csv/1',
            'description': ('Route using a csv file data source')
        },
        'csv / fetch':
        {
            'url':'earthquakes/csv/2',
            'description': ('Route using a csv file data source where the data file is '
            'retrieved from an external location such as github or S3')
        },
        'csv / fetch (d3.js)':
        {
            'url':'earthquakes/csv/3',
            'description': ('Route using a csv file data source where the data file is '
            'retrieved entirely under the control of javascript using d3.json() to fetch data.')
        },
        'json / local':
        {
            'url':'earthquakes/json/1',
            'description': ('Route using a json file data source')
        },
        'json / fetch':
        {
            'url':'earthquakes/json/2',
            'description': ('Route using a json file data source where the data file is '
            'retrieved from an external location such as github or S3')
        },
        'json / fetch (d3.js)':
        {
            'url':'earthquakes/json/3',
            'description': ('Route using a csv file data source where the data file is '
            'retrieved entirely under the control of javascript using d3.json() to fetch data.')
        }
    }

if __name__ == "__main__":
    app.run()

