import sqlite3

conn = sqlite3.connect("db.db")

c = conn.cursor()

c.execute("""CREATE TABLE pomodoro (
	user_id INTEGER, 
	count INTEGER,
    close INTEGER
  	)""")

conn.close()