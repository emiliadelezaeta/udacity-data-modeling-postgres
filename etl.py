import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
     This procedure processes a song file whose filepath has been provided as an argument.
     It extracts the song information in order to store it into the songs table.
     Then it extracts the artist information in order to store it into the artists table.

     INPUTS:
     * cur the cursor variable
     * filepath the file path to the song file
     """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id', 'year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
     This procedure processes a log file whose filepath has been provided as an argument.
     It extracts the user information in order to store it into the users table.
     Then it extracts the time information in order to store it into the time table.
     Execute the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.
     And for the last, it insert data into the fact table songplays

     INPUTS:
     * cur the cursor variable
     * filepath the file path to the log file
     """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')
    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ["start_time", "hour", "day", "week", "month", "year", "weekday"]
    time_df = pd.DataFrame(pd.to_numeric(time_data,  errors='ignore')).T
    time_df.columns = column_labels

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName","lastName","gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # convert column ts to timestamp
    df.ts = pd.to_datetime(df.ts, unit='ms')

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):

    """
         Procedure to get a list of all song JSON files in data/song_data
         And also it gets a list of logs of all logs files in data/log_data

         INPUTS:
         cur the cursor variable.
         the connection to sparkifydb in postgres.
         path to the folder where the files are
         and the function to be called process_song_file or process_log_file.
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
        Open the connection to postgres database
        Call the functions to process and insert data coming from song and log files
    """

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()