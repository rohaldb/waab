from app import app
from flask import request, jsonify, json
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import json
from flask_pymongo import PyMongo
from app.programs import *
from app.services.functions import *
from app.services.pdf_parser import PdfParser


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def home():
    print(len(request.files))
    bytestream = request.files.get('file')
    data = PdfParser.open_and_extract(bytestream)
    program_code = '3707'
    # with open('./programs.json', 'r') as f:
    #     program_dict = json.load(f)
    # print(program_dict)
    have_to_do = set(programs.get(program_code))
    already_done = set(data.get('Courses').copy())
    remaining = have_to_do - already_done
    # for r in have_to_do:
    #     if r in already_done:
    #         remaining.remove(r)
    data = list(remaining)
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
