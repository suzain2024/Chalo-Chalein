import sqlite3
conn=sqlite3.connect("railway.db")
cursor=conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS TRAINS(TRAIN_ID INTEGER PRIMARY KEY,
               TRAIN_NAME TEXT,
               SOURCE TEXT,
               DESTINATION TEXT,
               DATE TEXT,
               SEATS INTEGER)""") #text is used for string datatype in sqlite

cursor.execute("""(
    CREATE TABLE IF NOT EXISTS BOOKINGS(
        BOOKING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TRAIN_ID INTEGER,
        USER_NAME TEXT,
        SEAT_NO INTEGER,
        STATUS TEXT
    ) 
)""")

conn.commit()#finalizes the transaction
conn.close()#closes the transaction


