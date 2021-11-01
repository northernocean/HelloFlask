import csv
import sqlite3
import pandas as pd
from datetime import datetime

def main():
    
    import_method = 2

    # -------------------------------------------------------------------
    # import with sqlite library - explicitly creating and inserting rows
    # -------------------------------------------------------------------
    if(import_method == 1):

        con = sqlite3.connect('DAT.sqlite3') # database file input
        cur = con.cursor()
        cur.executescript("""
            DROP TABLE IF EXISTS earthquakes;
            CREATE TABLE earthquakes (
            Date TIMESTAMP, Time TIMESTAMP, Latitude REAL, 
            Longitude REAL, Type TEXT, Depth REAL, 
            DepthError REAL, DepthSeismicStations INTEGER, Magnitude REAL,
            MagnitudeType TEXT, MagnitudeError REAL, MagnitudeSeismicStations INTEGER,
            AzimuthalGap REAL, HorizontalDistance REAL, HorizontalError REAL,
            RootMeanSquare REAL, ID TEXT, Source TEXT,
            LocationSource TEXT, MagnitudeSource TEXT, Status TEXT
                );
            """) # checks to see if table exists and makes a fresh table.

        with open('database.csv', "r") as f: # CSV file input
            reader = csv.reader(f, delimiter=',') # no header information with delimiter
            next(reader)
            for row in reader:
                # sqlite handles the dates best when they are in yyyy-mm-dd format
                a,b,c = row[0].split("/")
                row[0] = c + '-' + a + '-' + b
                sql = """
                    insert into earthquakes (
                        Date, Time, Latitude, 
                        Longitude, Type, Depth, 
                        DepthError, DepthSeismicStations, Magnitude,
                        MagnitudeType, MagnitudeError, MagnitudeSeismicStations,
                        AzimuthalGap, HorizontalDistance, HorizontalError,
                        RootMeanSquare, ID, Source,
                        LocationSource, MagnitudeSource, Status)
                    values (
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ? );
                """
                cur.execute(sql, row)
            con.commit()
        con.close() # closes connection to database

    # ------------------
    # import with pandas
    # ------------------
    if(import_method == 2):

        # did not find infer_datetime_format=True to work correctly,
        # so importing the dates as strings and converting to
        # to dates use the pd.to_datetime method
        df = pd.read_csv('database.csv', infer_datetime_format=False)
        df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
        df['Time'] = pd.to_datetime(df['Time'], format="%H:%M:%S")
        
        con = sqlite3.connect('DAT.sqlite3') # database file input
        df.to_sql('earthquakes', con, if_exists='replace', index=False)
        con.close()


if __name__=='__main__':
    main()