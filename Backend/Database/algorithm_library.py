import sqlite3
from pprint import pprint as pp
from algorithm_data import *

db_path='speedcubing.db'

def insert_methods_and_algorithm_categories():
    # this is for cfop currently. will do roux later!
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute('''INSERT OR IGNORE INTO Methods (Name) VALUES ('CFOP')''')
    cursor.execute('''INSERT OR IGNORE INTO Methods (Name) VALUES ('ROUX')''')
    for category in ['F2L', 'OLL', 'PLL']:
        cursor.execute('''
        INSERT OR IGNORE INTO AlgorithmCategories (MethodID, Name)
        VALUES (
            (SELECT MethodID
            FROM Methods
            WHERE Name='CFOP'), ?)
            ''', (category,))
        
    connection.commit()
    connection.close()
    print('Methods and algorithm category for CFOP is inserted!')
    
def insert_f2l_algorithms_into_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    for category_name, case_name, notation in f2l_algorithms:
        cursor.execute('''
        INSERT OR IGNORE INTO Algorithms (CategoryID, Name, Notation)
        VALUES (
            (SELECT CategoryID FROM AlgorithmCategories WHERE Name=?), ?, ?)''', (category_name, case_name, notation))

    connection.commit()
    connection.close()
    print('F2L algorithms have been added into the Algorithms table!')

def insert_oll_algorithms_into_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    for category_name, state, notation in oll_algorithms:
        cursor.execute('''
        INSERT OR IGNORE INTO Algorithms (CategoryID, Name, Notation)
        VALUES (
            (SELECT CategoryID FROM AlgorithmCategories WHERE Name=?), ?, ?)''', (category_name, state, notation))

    connection.commit()
    connection.close()
    print('OLL algorithms have been added into the Algorithms table!')

def insert_pll_algorithms_into_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    for category_name, case_name, notation in pll_algorithms:
        cursor.execute('''
        INSERT OR IGNORE INTO Algorithms (CategoryID, Name, Notation)
        VALUES (
            (SELECT CategoryID FROM AlgorithmCategories WHERE Name=?), ?, ?)''', (category_name, case_name, notation))

    connection.commit()
    connection.close()
    print('PLL algorithms have been added into the Algorithms table!')

if __name__ == '__main__':
    insert_methods_and_algorithm_categories()
    insert_f2l_algorithms_into_table()
    insert_oll_algorithms_into_table()
    insert_pll_algorithms_into_table()