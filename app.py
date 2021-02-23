import datetime
import sqlite3

from flask import Flask, request, Response, render_template

from flask_cors import CORS


_database_name = 'blog-post.db'


def init_sqlite_database():
    conn = sqlite3.connect(_database_name)
    print("The database was opened successfully...")

    # Create a table called "post" which we will use to store our blog posts.
    conn.execute('CREATE TABLE IF NOT EXISTS post (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, author TEXT, date TEXT)')
    print("'post'" + " table was created successfully...")
    conn.close()


init_sqlite_database()


app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/index')
def show_index_page():
    return render_template('index.html')


@app.route('/add-new-post/', methods=["POST"])
def add_new_post():

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        author= request.form['author']

        # Create a response dictionary which will have all the necessary info we need.
        response = {
            'msg': None,
            'status_code': ''
        }
        try:
            with sqlite3.connect(_database_name) as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO post (title, description, author, date) VALUES (?, ?, ?, ?)", (title, description, author, datetime.datetime.now()))
                connection.commit()

                response['msg'] = "Blog post added successfully."
                response['status_code'] = Response().status_code

        except Exception as e:
            connection.rollback()
            response['msg'] = "Error occurred while inserting information in the database." + str(e)
            response['status_code'] = Response().status_code
        finally:
            connection.close()
            return response


@app.route('/get-all-posts/', methods=["GET", "POST"])
def get_all_post():

    if request.method == "POST" or request.method == "GET":

        # Create a dictionary which will have all the information we need.
        response = {
            'data': [],
            'msg': None,
            'status_code': ''
        }
        try:
            with sqlite3.connect(_database_name) as connection:
                # Connect to the database and select all the blog post that are in the db.
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM post")

                # Add everything inside the response dictionary.
                response['data'] = cursor.fetchall()
                response['msg'] = "Blog Posts were retrieved successfully from the database"
                response['status_code'] = Response().status_code

        except Exception as e:
            connection.rollback()
            response['msg'] = "Error occurred while retrieving blog posts in the database: " + str(e)
            response['status_code'] = Response().status_code
        finally:
            connection.close()
            return response
