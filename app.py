from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import secret

key_list = {
    'MongoKey': secret.mongo_db_key
}

# MongoDBConnection
client = MongoClient(key_list['MongoKey'])
db = client.dbsparta
todoCollection = db.todolist
pkCollection = db.pks

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    id_info = pkCollection.find_one({'collection_name': "todolist"})
    if id_info is None:
        doc = {
            'collection_name': 'todolist',
            'current_id': 0
        }
        pkCollection.insert_one(doc)
        current_id = 0
    else:
        current_id = int(id_info['current_id'])
    todo = request.form['todo']

    doc = {
        'num': current_id,
        'todo': todo,
        'done': 0
    }

    current_id += 1
    todoCollection.insert_one(doc)
    pkCollection.update_one({'collection_name': 'todolist'}, {'$set': {'current_id': current_id}})
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    todo_id = request.form['todo_id']
    todoCollection.update_one({'num': int(todo_id)}, {'$set': {'done': 1}})
    return jsonify({'msg': '업데이트 완료!'})


@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    todo_id = request.form['todo_id']
    todoCollection.update_one({'num': int(todo_id)}, {'$set': {'done': 0}})
    return jsonify({'msg': '업데이트 완료!'})


@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    todo_id = request.form['todo_id']
    todoCollection.delete_one({'num': int(todo_id)})
    return jsonify({'msg': '업데이트 완료!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(todoCollection.find({}, {'_id': False}))
    return jsonify({'bucketList': bucket_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8081, debug=True)