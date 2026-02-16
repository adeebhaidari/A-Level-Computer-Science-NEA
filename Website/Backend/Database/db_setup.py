import sqlite3
from pprint import pprint as pp

def setup_database(db_path='speedcubing.db'):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Forename TEXT NOT NULL,
        Middlename TEXT,
        Surname TEXT NOT NULL,
        EmailAddress TEXT NOT NULL UNIQUE,
        HashedPassword TEXT NOT NULL,
        JoinDate TEXT NOT NULL
    );''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FullSolves (
        SolveID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        Time REAL NOT NULL,
        MethodID INTEGER NOT NULL,
        State TEXT,
        Scramble TEXT NOT NULL,
        CubeBrand TEXT,
        SolveDate TEXT NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (MethodID) REFERENCES Methods(MethodID)
    );''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AlgorithmPractiseSolves (
        PractiseID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        AlgorithmID INTEGER NOT NULL,
        Time REAL NOT NULL,
        SolveDate TEXT NOT NULL,
        Notes TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (AlgorithmID) REFERENCES Algorithms(AlgorithmID)
    );''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Methods (
        MethodID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    );''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AlgorithmCategories (
        CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        MethodID INTEGER NOT NULL,
        Name TEXT NOT NULL,
        FOREIGN KEY (MethodID) REFERENCES Methods(MethodID)
    );''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Algorithms (
        AlgorithmID INTEGER PRIMARY KEY AUTOINCREMENT,
        CategoryID INTEGER NOT NULL,
        Name TEXT NOT NULL,
        Notation TEXT NOT NULL,
        FOREIGN KEY (CategoryID) REFERENCES AlgorithmCategories(CategoryID)
    );''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    setup_database()
    print('Database setup complete.')