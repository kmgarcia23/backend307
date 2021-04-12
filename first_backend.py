from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/users', methods = ['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username and search_job is None:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      elif search_username and search_job:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username and user['job'] == search_job:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
	   userToAdd = request.get_json()
	   userToAdd['id'] = gen_rand_ID()
	   users['users_list'].append(userToAdd)
	   resp = jsonify(name=userToAdd['name'],job=userToAdd['job'],id=userToAdd['id'],success=True)
	   resp.status_code = 201 #optionally, you can always set a response code. 
	   # 200 is the default code for a normal response
	   return resp
def gen_rand_ID():
	letsandnums = string.ascii_letters +string.digits
	randid = ""
	for i in range(6):
		randid += random.choice(letsandnums)
	return randid

@app.route('/users/<id>', methods = ['GET', 'DELETE'])
def get_user(id):
   if request.method == 'GET':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               return user 
         return ({})
      return users
   elif request.method == 'DELETE':
      if id:
         for user in users['users_list']:
            if user['id'] == id:
               users['users_list'].remove(user)
               resp = jsonify(success = True)
               resp.status_code = 204
               return resp
      resp = jsonify(success = False)
      resp.status_code = 404
      return resp

@app.route('/')
def hello_world():
    return 'Hello, World!'