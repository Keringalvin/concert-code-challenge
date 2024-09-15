
# Concert Database Project
Overview
This project involves managing a concert database using raw SQL queries. The database comprises three tables: Band, Venue, and Concert. The relationships between these tables are as follows:

A Band can perform in multiple concerts.
A Venue can host multiple concerts.
A Concert is associated with a specific band and venue, establishing a many-to-many relationship between bands and venues.
You will use Python's sqlite3 or psycopg2 library to interact with the database, running raw SQL commands to perform all CRUD (Create, Read, Update, Delete) operations. SQLAlchemy or any other ORM (Object-Relational Mapper) will not be used for this project.

# Schema
Tables
bands Table

name: String (The band's name)
hometown: String (The band's hometown)
sql
Copy code
CREATE TABLE bands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    hometown VARCHAR(255)
);
venues Table

title: String (The venue's name)
city: String (The venue's city)
sql
Copy code
CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    city VARCHAR(255)
);
concerts Table

band_id: Foreign key referencing the bands table
venue_id: Foreign key referencing the venues table
date: String (The date of the concert)
sql
Copy code
CREATE TABLE concerts (
    id SERIAL PRIMARY KEY,
    band_id INTEGER REFERENCES bands(id),
    venue_id INTEGER REFERENCES venues(id),
    date VARCHAR(255)
);
# Migrations
Before implementing the methods, you need to create and migrate the tables (bands, venues, and concerts). The concerts table will include foreign keys to establish relationships between the Band and Venue tables, as well as a date column to store the date of the concert.

 # Methods
Object Relationship Methods
Concert.band(): Returns the Band instance associated with the concert.
Concert.venue(): Returns the Venue instance associated with the concert.
Venue.concerts(): Returns a collection of all concerts at the venue.
Venue.bands(): Returns a collection of all bands that have performed at the venue.
Band.concerts(): Returns a collection of all concerts the band has performed in.
Band.venues(): Returns a collection of all venues the band has performed in.
Aggregate and Relationship Methods
Concert.hometown_show(): Returns True if the concert is in the band's hometown; otherwise, returns False. This is done by comparing the band's hometown with the concert's venue city.
Concert.introduction(): Returns a string with the band's introduction for this concert in the format:
arduino
Copy code
"Hello {venue city}!!!!! We are {band name} and we're from {band hometown}"
Band.play_in_venue(venue, date): Takes a venue (by title) and a date (as a string), and creates a new concert for the band at the specified venue on that date. Inserts the concert into the database using raw SQL.
Band.all_introductions(): Returns an array of strings representing all the introductions the band has made. Each introduction follows this format:
arduino
Copy code
"Hello {venue city}!!!!! We are {band name} and we're from {band hometown}"
Band.most_performances(): Returns the band that has performed in the most concerts. This is done by using SQL GROUP BY and COUNT to identify the band with the most concerts.
Venue.concert_on(date): Takes a date (string) and returns the first concert on that date at the venue.
Venue.most_frequent_band(): Returns the band that has performed the most at the venue, using a SQL GROUP BY query to count performances.
# Setup and Installation
Requirements
Python 3.x
sqlite3 (for SQLite database)
or psycopg2 (for PostgreSQL database)
Installation Steps
Clone the repository:

bash
Copy code
git https://github.com/Keringalvin/concert-code-challenge
cd concert-db
Install required packages: For SQLite:

bash
Copy code
# sqlite3 is included by default with Python
For PostgreSQL:

bash
Copy code
pip install psycopg2
Set up the database: For SQLite:

bash
Copy code
sqlite3 concerts.db < schema.sql
For PostgreSQL, modify the schema.sql to match PostgreSQL syntax, and then:

bash
Copy code
psql -U yourusername -d yourdatabase -f schema.sql
Run the project: Use the provided Python scripts to execute SQL queries and test the methods.

Example Usage
Below is an example of how to use the methods in Python:

python
Copy code
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('concerts.db')

# Example usage of the Band's methods
def get_band_concerts(band_id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM concerts WHERE band_id = ?', (band_id,))
    return cur.fetchall()

# Fetch all concerts for a band
band_concerts = get_band_concerts(1)
print(band_concerts)
Testing the Methods
To test the methods, insert sample data into the tables:

sql
Copy code
INSERT INTO bands (name, hometown) VALUES ('The Beatles', 'Liverpool');
INSERT INTO venues (title, city) VALUES ('Wembley Stadium', 'London');
INSERT INTO concerts (band_id, venue_id, date) VALUES (1, 1, '2024-09-20');
Then, call the methods in your Python code to ensure the raw SQL queries return the expected results.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# About
This project demonstrates how to build relationships and retrieve information from a concert database using raw SQL queries in Python, without the use of any ORM.

# Author
By Alvin kiptoo