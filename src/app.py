from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app =Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/py_mongo'
mongo = PyMongo(app)

#Routes

#users create
@app.route('/users', methods=['POST'])
def create_user():
    #receiving data
    #print(request.json)
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        #encrypt password
        hashed_password = generate_password_hash(password)
        #save to db
        id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password}
        )
        # user response
        res = {
            'id': str(id),
            'username': username, 
            'email': email, 
            'password': hashed_password
            }

        return res
    else:
        return not_found()

    return {'message': 'received'}

#list users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    res = json_util.dumps(users)
    return Response(res, mimetype='application/json')

#get user
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    res = json_util.dumps(user)
    return Response(res, mimetype="application/json")

#delete users
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    res = jsonify({'message': 'User '+ id + ' was deleted successfully'})
    return res


#update users
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        #encrypt password
        hashed_password = generate_password_hash(password)
        #update
        mongo.db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set':{
                'username': username,
                'password': hashed_password,
                'email': email
            }}
        )
        res = jsonify({'message': 'User '+id+' was updated successfully'})
        return res

# Receiving errors
@app.errorhandler(404)
def not_found(error=None):
    res = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    res.status_code = 404
    return res

if __name__ == "__main__":
    app.run(debug=True)