from flask import Flask, request


app = Flask(__name__)


@app.route('/add-new-post/', methods=["POST"])
def add_new_post():
    pass
