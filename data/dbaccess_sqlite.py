import os
import sqlite3

db_connection_string = None

# DATABASE_URL is a standard config variable set at heroku when you attach a postgres db
# the url at heroku will be in the form "postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE"

if 'DATABASE_URL' in os.environ:
    db_connection_string = os.environ['DATABASE_URL']
else:
    # or more elegantly, create a local DATABASE_URL environment variable
    # in which case you can omit the if/else and simply set the DB url to
    # the given value from your environment variable
    db_connection_string = 'data/DAT.sqlite3'


def test_connection():
    '''Attempts a DB connection with the default database'''
    try:
        print ('\ntesting db connection to ' + db_connection_string)
        cn = get_connection()
        if cn is not None:
            print('connection succeeded!\n')
        else:
            print('connection failed!\n')
    finally:
        if cn:
            cn.close()

def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(db_connection_string)
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