from app import app
from flask import request, jsonify, json
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from app.services.functions import *
from app.services.pdf_parser import PdfParser


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def hello():
    print(len(request.files))
    print(request.files.get('file'))
    bytestream = request.files.get('file')
    data = PdfParser.open_and_extract(bytestream)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

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
