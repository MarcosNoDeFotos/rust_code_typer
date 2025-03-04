
import sqlite3

def getDB():
    return sqlite3.connect("database.db", timeout=5)

def getSequence(tabla):
    cursor = getDB().cursor()
    cursor.execute(f"select seq from sqlite_sequence where name = '{tabla}'")
    seq = cursor.fetchone()[0]+1
    cursor.close()
    cursor.connection.close()
    return seq

sqlCursor = getDB().cursor()
sqlCursor.execute("create table if not exists sesiones(id varchar(40) primary key)")
sqlCursor.execute("create table if not exists codes(id integer primary key autoincrement, sesion varchar(40), codigo varchar(6))")



sqlCursor.close()
sqlCursor.connection.close()