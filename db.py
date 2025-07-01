from session_db import getSessionConnection


def createTables():
    connection = getSessionConnection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(20) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY(email)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        postId SERIAL PRIMARY KEY,
        username VARCHAR(20) NOT NULL,
        email VARCHAR(100) NOT NULL,
        title TEXT NOT NULL,
        publishDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        postContent TEXT NOT NULL,
        FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()
