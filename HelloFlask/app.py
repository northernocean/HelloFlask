from sqlite3.dbapi2 import Connection
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = None
    try:
        conn = sqlite3.connect('/app/HelloFlask/DAT.sqlite3')
    except:
        print("Error connecting to sqlite")
    return conn

def get_earthquake_count_by_years():
    cn = get_connection()
    xs = []
    ys = []
    if cn:
        cur = cn.cursor()
        cur.execute('''
        SELECT 
            strftime("%Y", "Date") AS "Year",
            COUNT("Date") AS "Total"
        FROM 
            earthquakes 
        GROUP BY 
            strftime("%Y", "Date");
        ''')
        rows = cur.fetchall()
        for row in rows:
            print(row)
            xs.append(row[0])
            ys.append(row[1])        
        cn.close() 
    
    return xs, ys


@app.route("/")
def index():
    xs, ys = get_earthquake_count_by_years()
    return render_template('index.html', data={'xs': xs, 'ys': ys})

if __name__ == "__main__":
    app.run()


