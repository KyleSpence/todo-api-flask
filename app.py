from flask import Flask, jsonify, abort, make_response, request
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure
from bson.json_util import dumps

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo = PyMongo(app)


def get_tasks_from_db():
  return list(mongo.db.tasks.find({}, {'_id': 0}))


def get_task_from_db(task_id):
  return list(mongo.db.tasks.find({"id": task_id}, {"_id": 0}))


def delete_task_from_db(task_id):
  mongo.db.tasks.delete_one({"id": task_id})


def update_task_from_db(task_id, task):
  mongo.db.tasks.update_one({"id": task_id}, {"$set": task}, upsert=False)


@app.errorhandler(404)
def not_found_error(error):
  return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/health')
def get_health():
  try:
    mongo.cx.admin.command("ismaster")
    return jsonify(success=True)
  except ConnectionFailure:
    abort(500)


@app.route('/todo/api/tasks', methods=['GET'])
def get_tasks():
  tasks = get_tasks_from_db()
  return jsonify({'tasks': tasks})


@app.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
  task = get_task_from_db(task_id)
  if len(task) == 0:
    abort(404)
  return jsonify({'task': task[0]})


@app.route('/todo/api/tasks', methods=['POST'])
def create_task():
  if not request.json or not 'title' in request.json:
    abort(400)
  tasks = get_tasks_from_db()

  task_id = 1
  if len(tasks) > 0:
    task_id = tasks[-1]['id'] + 1

  task = {
    'id': task_id,
    'title': request.json['title'],
    'description': request.json.get('description', ""),
    'done': False
  }
  task_object_id = mongo.db.tasks.insert_one(task).inserted_id

  if task_object_id:
    return jsonify({'success': True}), 201
  else:
    abort(400)


@app.route('/todo/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
  task = get_task_from_db(task_id)
  if len(task) == 0:
    abort(404)
  if not request.json:
    abort(400)
  if 'title' in request.json and type(request.json['title']) != str:
    abort(400)
  if 'description' in request.json and type(request.json['description']) is not str:
    abort(400)
  if 'done' in request.json and type(request.json['done']) is not bool:
    abort(400)
  task[0]['title'] = request.json.get('title', task[0]['title'])
  task[0]['description'] = request.json.get('description', task[0]['description'])
  task[0]['done'] = request.json.get('done', task[0]['done'])
  update_task_from_db(task_id, task[0])
  return jsonify({'success': True})


@app.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
  task = get_task_from_db(task_id)
  if len(task) == 0:
    abort(404)
  delete_task_from_db(task_id)
  return jsonify({'result': True})


if __name__ == '__main__':
  app.run(debug=True)
