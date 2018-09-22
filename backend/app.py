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
    # return str(online_users)

if __name__ == "__main__":
    app.run(debug=True)
