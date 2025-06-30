import mysql.connector as mysql
from session_db import getSessionConnection


def getDatabaseConnection():  # Connects to the database
    session = getSessionConnection()
    cursor = session.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS textopia_database")
    session.database = "textopia_database"
    return session


def createTables():  # Create the tables
    connection = getDatabaseConnection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(20) NOT NULL unique,
        email VARCHAR(100) NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY(email)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        postId INT NOT NULL AUTO_INCREMENT,
        username VARCHAR(20) NOT NULL,
        email VARCHAR(100) NOT NULL,
        title TEXT NOT NULL,
        publishDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        postContent TEXT NOT NULL,
        PRIMARY KEY(postId),
        FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()
