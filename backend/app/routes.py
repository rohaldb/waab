from app import app
from flask import request, jsonify, json
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import json
from flask_pymongo import PyMongo
from app.programs import *
from app.courses import comp_courses
from app.services.functions import *
from app.services.pdf_parser import PdfParser


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def home():
    print(len(request.files))
    bytestream = request.files.get('file')
    data = PdfParser.open_and_extract(bytestream)
    program_code = '3707'
    have_to_do = set(programs.get(program_code))
    already_done = set(data.get('Courses').copy())
    remaining = have_to_do - already_done
    # for r in have_to_do:
    #     if r in already_done:
    #         remaining.remove(r)
    print(remaining)
    output = list(remaining)
    course_metadata = []
    for course_code in output:
        for c in comp_courses:
            if c.get("course") == course_code:
                course_metadata.append({'course': course_code, 'prereqs': c.get("prereqs"), 'sems': c.get("sems"), 'des': c.get("des")})
    print(course_metadata)
    response = app.response_class(
        response=json.dumps([output, list(already_done), course_metadata]),
        status=200,
        mimetype='application/json'
    )
    return response
