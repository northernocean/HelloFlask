import requests
import csv
import io
import pandas as pd
import numpy as np

DATA_SOURCE = "csv remote file storage/pandas"
url = 'https://raw.githubusercontent.com/northernocean/HelloFlask/main/data/dat.csv'
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
            data_df = pd.read_csv(url)
            data_df['Date'] = pd.to_datetime(data_df['Date'])
            data_df['Time'] = pd.to_datetime(data_df['Time'])
        except Exception as ex:
            data_df = None
    return data_df.copy(deep=True)


def test_connection():
    print ('\ntesting db connection to remote csv file storage')
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
        ys = [int(element) for element in ys] #convert numpy int dtypes to plain python ints to avoid json serialization errors
    return xs, ys


def in_memory_string_file():
    # based on example from 
    #     https://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
    # Interesting approach but the pandas option is better since we will want to manipulate the data in a dataframe anyway... 
    
    response = requests.get(url)
    csv_bytes = response.content

    # write in-memory string file from bytes, decoded (utf-8)
    str_file = io.StringIO(csv_bytes.decode('utf-8'), newline='\n')
        
    reader = csv.reader(str_file)
    for row_list in reader:
        print(row_list)

    str_file.close()

if __name__ == "__main__":
    test_connection()
