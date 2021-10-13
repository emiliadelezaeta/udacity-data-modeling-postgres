# Data Modeling with Postgres

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description

In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Data Model 

This project use a single fact table to store measure data *(songplays)* and few dimension tables to store some attributes about data.

![](udacity-sparkifydb-data-model.jpg)

**songplays** --> records in log data associated with song plays i.e. records with page ```NextSong```.

**users** --> users in the app.

**songs** --> songs in music database.

**artists** --> artists in music database.

**time** --> timestamps of records in **songplays** broken down into specific units.

## ETL Pipeline

There are few steps to run in order to insert data into the tables.

**sql_queries.py** --> DDL to create the structure of the database and DML to insert and manipulate data in the database.

**create_tables.py** --> connect to a default database and drop/create a new database named ```sparkifydb``` and call the previous step.

**etl.py** --> read, transform and load data into the new database.

## Example Queries

See by users what songs they have listened to, when and the artist

```
SELECT a.start_time
    , CONCAT(b.first_name, ' ', b.last_name) as user_name
    , c.name as artist_name
    , d.title as song_title 
FROM songplays a 
JOIN users b ON a.user_id = b.user_id 
JOIN artists c ON a.artist_id = c.artist_id 
JOIN songs d ON a.song_id = d.song_id 
JOIN time t ON a.start_time = t.start_time
WHERE a.song_id <> 'None'
```

Analyze which day of the week there are more reproductions

```
SELECT t.weekday, count(*) total 
FROM songplays a 
JOIN time t ON a.start_time = t.start_time 
GROUP BY t.weekday 
ORDER BY 2 DESC;

```

Note: [Weekday Function In Python](https://pythontic.com/datetime/date/weekday)