import requests
import csv
import io
import pandas as pd
import numpy as np

DATA_SOURCE = "json file"
uri = 'data/dat.json'
data_df = None

# Notes:
# The column for MagnitudeSeismicStations is stored as a float in this
#     pandas dataframe, whereas it is a int in postgres/sqlite databases.

def get_connection():
    '''for a csv data source we do not really "connect" to the datasource as would
       happen with a database. Instead, we retrieve the data and hold it locally
       in a pandas dataframe - which we can then treat as in-memory data source'''
    global data_df
    if data_df is None:
        try:
            data_df = pd.read_json(uri)
            data_df['Date'] = pd.to_datetime(data_df['Date'])
            data_df['Time'] = pd.to_datetime(data_df['Time'])
        except Exception as ex:
            data_df = None
    return data_df.copy(deep=True)


def test_connection():
    print ('\ntesting db connection to remote json file storage')
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
