from flask import Flask, render_template
import dbaccess as db
from dotenv import load_dotenv
from time import sleep
load_dotenv()
app = Flask(__name__)

sleep(1)
db.test_connection()

@app.route("/")
def index():
    xs, ys = db.get_earthquake_count_by_years()
    print('here')
    print(xs)
    print(ys)
    return render_template('index.html', data={'xs': xs, 'ys': ys})

if __name__ == "__main__":
    app.run()


