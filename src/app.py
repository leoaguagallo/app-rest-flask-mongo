from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app =Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/py_mongo'
mongo = PyMongo(app)

#Routes
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
        return {'message': 'Fail'}

    return {'message': 'received'}

if __name__ == "__main__":
    app.run(debug=True)