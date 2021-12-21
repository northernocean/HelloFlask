import sqlite3

DATA_SOURCE = "sqlite"
db_connection_string = 'data/dat.sqlite3'


def test_connection():
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
    except Exception as ex:
        print(ex)
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