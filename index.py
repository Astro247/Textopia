from flask import Flask, render_template, jsonify, request, session
from utils import registerUser, loginUser, getProfileInfo, addPostToDatabase, getAllPosts
from db import createTables
from secretkey import returnSecretKey

app = Flask(__name__)
app.secret_key = returnSecretKey()


@app.route('/')
def goToHomepage():
    posts = getAllPosts()
    return render_template('home.html', page="home", posts=posts)


@app.route('/login')
def goToLogin():
    return render_template('login.html', page="login", logged_in="user_email" in session)


@app.route('/register')
def goToRegister():
    return render_template('register.html', page="register", logged_in="user_email" in session)


@app.route('/register', methods=['POST'])
def addUserInfo():
    datas = request.get_json()
    username = datas['username']
    email = datas['email']
    password = datas['password']
    result = registerUser(username, email, password)
    return jsonify(result)


@app.route('/login', methods=['POST'])
def logUserInfo():
    datas = request.get_json()
    email = datas['email']
    password = datas['password']
    result = loginUser(email, password)
    if result['success']:
        session['user_email'] = email
        return {"success": True}
    return {"success": False, "error": result['error']}


@app.route('/profile')
def goToProfile():
    return render_template('profile.html', page="profile", logged_in="user_email" in session)


@app.route('/getProfile')
def profileInfo():
    email = session.get("user_email")
    result = getProfileInfo(email)
    return jsonify(result)


@app.route('/logout')
def logout():
    session.clear()
    return goToHomepage()


@app.route('/post')
def goToPost():
    return render_template('post.html', page="post", logged_in="user_email" in session)


@app.route('/createPost', methods=["POST"])
def createPost():
    datas = request.get_json()
    email = session.get("user_email")
    title = datas['title']
    content = datas['content']
    result = addPostToDatabase(email, title, content)
    return jsonify(result)


def create_app():
    createTables()
    return app


if __name__ == '__main__':
    app.run()
