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

def get_schedule(courses):
    pairs = unroll(courses)
    n = len(pairs)
    return find_order(n, pairs)

"""
eg. courses:
{ COMP3121: [COMP1917, COMP1927]}
"""
def unroll(courses):
    output = []
    for c in courses:
        for p in c:
            output.append([c, p])
    return output

"""
assumes input is:
[course, prereq]
"""
def find_order(n, pairs):
    graph = [[] for _ in range(n)]
    outdegree = [0] * n

    for course, pre in pairs:
        graph[course].append(pre)
        outdegree[pre] += 1

    bfs = [
        course
        for course in range(n)
        if outdegree[course] == 0 # This course is not a prereq for anything
    ]
    for course in bfs:
        for pre in graph[course]:
            outdegree[pre] -= 1
            if outdegree[pre] == 0:
                bfs.append(pre)

    return bfs[::-1] if len(bfs) == n else []


if __name__ == "__main__":
    app.run(debug=True)
