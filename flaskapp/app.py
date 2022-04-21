from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket

app = Flask(__name__)
MONGO_USER = 'root'
MONGO_PASS = 'pass'
hostname = socket.gethostname()
MONGO_HOST = str(socket.gethostbyname(hostname))
MONGO_HOST = 'mongo'
print(MONGO_HOST)
MONGO_PORT = 27017
MONGO_DB = 'mydb'
app.config["MONGO_URI"] = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
mongo = PyMongo(app)
db = mongo.db

# uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
# client = MongoClient(host= socket.gethostname() , port= 27017, username= 'root', password= 'pass', authSource="admin", )
# db_obj = client[db_name]
# db= db_obj

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to Tasks app! I am running inside {} pod!".format(hostname)
    )

@app.route("/tasks")
def get_all_tasks():
    tasks = db.task.find()
    data = []
    for task in tasks:
        item = {
            "id": str(task["_id"]),
            "task": task["task"]
        }
        data.append(item)
    return jsonify(
        data=data
    )

@app.post("/task")
def create_task():
    data = request.get_json(force=True)
    db.task.insert_one({"task": data["task"]})
    return jsonify(
        message="Task saved successfully!"
    )


@app.put("/task/<id>")
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = db.task.update_one({"_id": ObjectId(id)}, {"$set": {"task": data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )

@app.delete("/task/<id>")
def delete_task(id):
    response = db.task.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )


@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    db.task.remove()
    return jsonify(
        message="All Tasks deleted!"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)