# create SQLite database and tables etc
import sqlite3
from pprint import pprint as pp

# this creates a new database and connects to it if it doesnt already exist
# else it will just connect to that existing one
connection = sqlite3.connect('SpeedCubing.db')

# creates a cursor to do all kinds of things e.g. create a table
cursor = connection.cursor()

# creating the tables in the database
# form: name, datatype
# the user ID which is the primary key is automatically made with SQLite3, you need to specify it yourself when wanting to look at the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Forename TEXT,
    Middlename TEXT,
    Surname TEXT,
    EmailAddress TEXT,
    HashedPassword TEXT,
    JoinDate TEXT
)''')

many_users = [('Bob', 'None', 'Bill', 'bob@yahoo.com', 'passss', '13/05/25'),
              ('John', 'David', 'Howard', 'john@yahoo.com', 'nooneknows', '14/05/25'),
              ('Eve', 'Sanderson', 'John', 'eve@gmail.com', 'cubing!!', '16/08/25')]

cursor.executemany('''
                   INSERT INTO Users (Forename, Middlename, Surname, EmailAddress, HashedPassword, JoinDate) 
                   VALUES (?,?,?,?,?,?)''', 
                   many_users)

# query the database
cursor.execute('''
               SELECT * 
               FROM Users 
               WHERE rowid > 1''')

'''
pp(cursor.fetchone()) returns the first one
pp(cursor.fetchmany(2)) returns the first x amount you specify
pp(cursor.fetchall())
'''

# formatting results
data_items = cursor.fetchall() # a list of tuples now!
for item in data_items:
    pp(item)
    # pp(item[1]) # as this is a tuple, you can index it like normal

# this commits the command, now we can close the connect if you want to
connection.commit()
connection.close()