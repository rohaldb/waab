from app import app
from flask import request, jsonify, json
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import json
from flask_pymongo import PyMongo
from app.programs import *
from app.courses import comp_courses
from app.services.functions import *
from app.services.pdf_parser import PdfParser, CourseMatcher


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def home():
    print(len(request.files))
    bytestream = request.files.get('file')
    array_of_courses, course_meta_data, program_code = PdfParser.open_and_extract(bytestream)
    have_to_do = set(course_meta_data.get(program_code))
    already_done = set(array_of_courses)
    remaining = have_to_do - already_done

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
