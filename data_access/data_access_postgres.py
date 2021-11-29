import psycopg2
import os

DATA_SOURCE = ""
db_connection_string = ""
local_connection_string = 'postgres://max:fiddle-rain-stones@192.168.0.186:5432/moondust'

# DATABASE_URL is a standard config variable set at heroku when you attach a postgres db
# the url at heroku will be in the form "postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE"

if 'DATABASE_URL' in os.environ:
    db_connection_string = os.environ['DATABASE_URL']
    DATA_SOURCE = "postgres (production)"
else:
    # or more elegantly, create a local DATABASE_URL environment variable
    # in which case you can omit the if/else and simply set the DB url to
    # the given value from your environment variable
    db_connection_string = local_connection_string
    DATA_SOURCE = "postgres (development)"


def get_connection():
    #pyscopg2.connect(host=ADDRESS, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
    #pyscopg2.connect('postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE')
    cn = psycopg2.connect(db_connection_string)
    return cn


def test_connection():
    '''Attempts a DB connection with the default database'''
    try:
        print ('\ntesting db connection to ' + db_connection_string.split('@')[1])
        cn = get_connection()
        if cn is not None:
            print('connection succeeded!\n')
        else:
            print('connection failed!\n')
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
            # print(row)
            xs.append(row[0])
            ys.append(row[1])        
    except Exception as ex:
        print(ex)
    finally:
        if cn:
            cn.close()
            print('connection closed')
    return xs, ys