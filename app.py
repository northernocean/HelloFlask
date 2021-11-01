import os
from flask import Flask, render_template

try:
    ENVIRONMENT = os.environ["RUNTIME_ENVIRONMENT"]
except:
    ENVIRONMENT = "Development"

if ENVIRONMENT == 'Production':
    import dbaccess_sqlite as db
else:
    import dbaccess_sqlite as db

app = Flask(__name__)

@app.route("/")
def index():
    xs, ys = db.get_earthquake_count_by_years()
    return render_template('index.html', data={'xs': xs, 'ys': ys})

if __name__ == "__main__":
    app.run()


