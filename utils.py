from session_db import getSessionConnection
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras


def registerUser(username, email, password):
    connection = getSessionConnection()
    cursor = connection.cursor()

    # Check if email already registered
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return {"success": False, "error": "Email already registered."}

    # Check if username taken
    cursor.execute(
        "SELECT username FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return {"success": False, "error": "Username already taken."}

    hashed_password = generate_password_hash(password)

    # Insert user
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"success": True}


def loginUser(email, password):
    connection = getSessionConnection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, password FROM users WHERE email = %s",
        (email,)
    )
    row = cursor.fetchone()

    if row:
        username, stored_hash = row
        if check_password_hash(stored_hash, password):
            cursor.close()
            connection.close()
            return {"success": True, "username": username}
        else:
            cursor.close()
            connection.close()
            return {"success": False, "error": "Wrong password"}
    else:
        cursor.close()
        connection.close()
        return {"success": False, "error": "User not registered"}


def getProfileInfo(email):
    connection = getSessionConnection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT username, email FROM users WHERE email = %s",
        (email,)
    )
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row:
        return {"username": row[0], "email": row[1]}
    else:
        return None


def addPostToDatabase(email, title, content):
    if title == "" or content == "":
        return {"success": False}

    connection = getSessionConnection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, email FROM users WHERE email = %s",
        (email,)
    )
    row = cursor.fetchone()
    if not row:
        cursor.close()
        connection.close()
        return {"success": False, "error": "User not found"}

    userUsername = row[0]
    userEmail = row[1]

    cursor.execute(
        "INSERT INTO posts (username, email, title, postContent) VALUES (%s, %s, %s, %s)",
        (userUsername, userEmail, title, content)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"success": True}


def getAllPosts():
    connection = getSessionConnection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT username, title, publishdate, postContent
        FROM posts
        ORDER BY publishdate DESC
    """)
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return posts
