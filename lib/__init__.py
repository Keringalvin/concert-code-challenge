import sqlite3

CONN = sqlite3.connect('the_database.db')
CURSOR = CONN.cursor()