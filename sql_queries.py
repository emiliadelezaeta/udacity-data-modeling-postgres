# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXIST songplay;"
user_table_drop = "DROP TABLE IF EXIST user;"
song_table_drop = "DROP TABLE IF EXIST song;"
artist_table_drop = "DROP TABLE IF EXIST artist;"
time_table_drop = "DROP TABLE IF EXIST time;"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXIST songplay (
                            songplay_id INT, 
                            start_time TIMESTAMP,
                            user_id INT NOT NULL,
                            level VARCHAR,
                            song_id INT NOT NULL,
                            artist_id INT NOT NULL,
                            session_id INT NOT NULL,
                            location VARCHAR,
                            user_agent VARCHAR,
                            PRIMARY KEY (songplay_id)
                            );
""")

user_table_create = ("""CREATE TABLE IF NOT EXIST users(
                            user_id INT,
                            first_name VARCHAR NOT NULL,
                            last_name VARCHAR NOT NULL,
                            gender VARCHAR,
                            level VARCHAR,
                            PRIMARY KEY(user_id)                    
                            );
""")

song_table_create = ("""CREATE TABLE IF NOT EXIST song(
                            song_id INT, 
                            title INT NOT NULL, 
                            artist_id INT NOT NULL, 
                            year INT, 
                            duration NUMERIC,
                            PRIMARY KEY (song_id)
                            );
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]