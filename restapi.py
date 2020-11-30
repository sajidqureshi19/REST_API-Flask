from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
app.config["MONGO_URI"] = <DB_URI>
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    response = mongo.db.users.find()
    for doc in response:
        print("This is response " + str(doc))
        doc['_id'] = str(doc['_id'])
    return doc


@app.route('/users/post', methods=['POST'])
def post_user():
    name = request.json['name']
    year = request.json['year']
    new_id = mongo.db.users.insert({'name': name, 'year': year})
    new_data = mongo.db.users.find_one({'_id': new_id})
    output = {'name': new_data['name'], 'year': new_data['year']}
    return jsonify({'result': output})


@app.route('/user/<username>', methods=['GET'])
def user_profile(username):
    user = mongo.db.users.find_one({'name': username})
    print('This is single user' + str(user))
    return user


@app.route('/user/delete/<name>', methods=['DELETE'])
def delete_user(name):
    mongo.db.users.delete_one({'name': name})
    response = jsonify('User deleted successfully!')
    return response


if __name__ == "__main__":
    app.run(debug=True)
