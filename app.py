from flask import Flask, render_template
from dotenv import load_dotenv
import dbaccess as db

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    xs, ys = db.get_earthquake_count_by_years()
    return render_template(
        'index.html',
        data={'xs': xs, 'ys': ys, 'data_source': db.DATA_SOURCE})


@app.route("/api/earthquakes")
def earthquakes():
    return "it works!"

if __name__ == "__main__":
    app.run()

