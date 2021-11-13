import psycopg2
import os

db_url = None

# DATABASE_URL is a standard config variable set at heroku when you attach a postgres db
# the url at heroku will be in the form "postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE"

if 'DATABASE_URL' in os.environ:
    db_url = os.environ['DATABASE_URL']
else:
    # or more elegantly, create a local DATABASE_URL environment variable
    # in which case you can omit the if/else and simply set the DB url to
    # the given value from your environment variable
    db_url = 'postgres://max:fiddle-rain-stones@192.168.0.186:5432/moondust'


def get_connection():
    #pyscopg2.connect(host=ADDRESS, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
    #pyscopg2.connect('postgres://USER:PASSWORD@ADDRESS:PORT/DATABASE')
    cn = psycopg2.connect(db_url)
    return cn

def get_earthquake_count_by_years():
    try:
        cn = get_connection()
        xs = []
        ys = []
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
            # print(row)
            xs.append(row[0])
            ys.append(row[1])        
    except Exception as ex:
        print(ex)
    finally:
        if cn:
            cn.close()
    return xs, ys