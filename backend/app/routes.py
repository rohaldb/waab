from app import app
from flask import request
from flask_pymongo import PyMongo
from app.services.functions import *

@app.route("/", methods=['GET', 'POST'])
def hello():
    #print(len(request.files))
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
