import psycopg2
import os

DATA_SOURCE = ""
db_connection_string = ""

# DATABASE_URL is a standard config variable set at heroku when you attach a postgres db
# and the url at heroku will be in the form "postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE"
# For local development the postgres connection string can be placed in the same environment
# variable, or it can be hard-coded in as shown below.

if 'DATABASE_URL' in os.environ:
    db_connection_string = os.environ['DATABASE_URL']
    if '192.168.0' in db_connection_string:
        DATA_SOURCE = "postgres (development)"
    else:
        DATA_SOURCE = "postgres (production)"
else:
    db_connection_string = 'postgres://<user>:<password>@192.168.0.1:5432/<database>'
    DATA_SOURCE = "postgres (development)"


def get_connection():
    try:
        # pyscopg2.connect(host=ADDRESS, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
        # pyscopg2.connect('postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE')
        cn = psycopg2.connect(db_connection_string)
    except Exception as ex:
        print(ex)
        cn = None
    return cn


def test_connection():
    try:
        print ('\ntesting db connection to ' + db_connection_string.split('@')[1])
        cn = get_connection()
        if cn is not None:
            print('connection succeeded!\n')
    finally:
        if cn:
            cn.close()


def get_earthquake_count_by_years():
    try:
        cn = get_connection()
        xs = []
        ys = []
        cur = cn.cursor()
        cur.execute('''
        SELECT 
            EXTRACT(YEAR FROM "Date") AS "Year",
            COUNT("Date") AS "Total"
        FROM 
            earthquakes 
        GROUP BY 
            EXTRACT(YEAR FROM "Date");
        ''')
        rows = cur.fetchall()
        for row in rows:
            xs.append(row[0])
            ys.append(row[1])        
    except Exception as ex:
        print(ex)
    finally:
        if cn:
            cn.close()
            print('connection closed')
    return xs, ys


if __name__ == "__main__":
    test_connection()