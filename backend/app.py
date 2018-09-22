
from app import app
from flask import Flask
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/", methods=['GET', 'POST'])
def hello():
    print(len(request.files))
    return 'hi'

@app.route("/courses", methods=["GET", "POST"])
def get_course():
    if request.method == "POST":
        degree_code = request.form['code']
        req_courses = models.get_required_courses(degree_code)
        done_courses = models.get_done_courses(user)
        for r in req_courses:
            if r in done_courses:
                req_courses.remove(r)
        return req_courses


if __name__ == "__main__":
    app.run(debug=True)
