from pymongo import MongoClient
import os
import pandas as pd
import numpy as np

DATA_SOURCE = "mongodb"
mongo_connection_string = 'mongodb://david:windy-chance@192.168.0.186:27017/calico'
conn = ''
data_df = None

if 'MONGO_CONN' in os.environ:
    conn = os.environ['MONGO_URI']
    DATA_SOURCE = "mongodb (production)\n\nPRODUCTION MONGODB NOT SUPPORTED"
else:
    # or more elegantly, create a local DATABASE_URL environment variable
    # in which case you can omit the if/else and simply set the DB url to
    # the given value from your environment variable
    conn = mongo_connection_string
    DATA_SOURCE = "mongodb (development)"

# Notes:
# The column for MagnitudeSeismicStations is stored as a float in this
#     pandas dataframe, whereas it is a int in postgres/sqlite databases.

def get_connection():
    global data_df
    if data_df is None:
        try:
            client = MongoClient(conn)
            db = client['calico']['earthquakes']
            data_df = pd.DataFrame(list(db.find()))
            data_df['Date'] = pd.to_datetime(data_df['Date'])
            data_df['Time'] = pd.to_datetime(data_df['Time'])
        except Exception as ex:
            data_df = None
    return data_df.copy(deep=True)


def test_connection():
    print ('\ntesting connection to mongodb')
    df = get_connection()
    if df is None:
        print("Connection failed!")
    else:
        print("Connection succeeded!")


def get_earthquake_count_by_years():
    xs = []
    ys = []
    df = get_connection()
    if df is not None:
        df['Year'] = df['Date'].dt.year
        df_filtered = df.groupby('Year')['ID'].count()
        xs = list(df_filtered.index)
        ys = list(df_filtered.values)
        ys = [int(element) for element in ys] #convert numpy ints to plain python ints to avoid later json serialization errors in flask
    return xs, ys


if __name__ == "__main__":
    test_connection()
