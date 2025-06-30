from db import getDatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash


def registerUser(username, email, password):
    connection = getDatabaseConnection()
    cursor = connection.cursor()

    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return {"success": False, "error": "Email already registered."}

    cursor.execute(
        "SELECT username FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return {"success": False, "error": "Username already taken."}

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return {"success": True}


def loginUser(email, password):
    connection = getDatabaseConnection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, password FROM users WHERE email = %s", (email,))
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
    connection = getDatabaseConnection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT username, email FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return {"username": row[0], "email": row[1]}


def addPostToDatabase(email, title, content):
    connection = getDatabaseConnection()
    cursor = connection.cursor()
    if title == "" or content == "":
        return {"success": False}
    cursor.execute(
        "SELECT username, email FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    userUsername = row[0]
    userEmail = row[1]
    postDatas = (userUsername, userEmail, title, content)
    cursor.execute(
        "INSERT INTO posts (username, email, title, postContent) VALUES (%s, %s, %s, %s)", postDatas)
    connection.commit()
    cursor.close()
    connection.close()
    return {"success": True}


def getAllPosts():
    connection = getDatabaseConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT username, title, publishDate, postContent
        FROM posts
        ORDER BY publishDate DESC
    """)
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return posts
