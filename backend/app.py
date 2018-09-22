from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def hello():
    online_users = mongo.db.users.find({"online": True})
    return str(online_users)

if __name__ == "__main__":
    app.run(debug=True)
