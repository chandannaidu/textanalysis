from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimlarityDB
users = db["Users"]

def UserExist(username):
    if users.find({"username":username}).count() == 0 :
        return False
    else:
        return True

def verifyPW(username, password):
    pass

def count_Tokens(username):
    pass

class Regiester (Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status" : 301,
                "msg" : "Invalid Username"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        users.insert({
            "Username" : username,
            "Password" : hashed_pw,
            "Tokens" : 6

        })

        retJson = {
                "status" : 200,
                "msg" : "you have successfully signed up to an API "
            }
        jsonify(retJson)
    
class detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if UserExist(username):
            retJson = {
                "status" : 301,
                "msg" : "Invalid Username"
            }
            return jsonify(retJson)

        correct_pw = verifyPW(username, password)

        if not correct_pw:
            retJson = {
            "status" : 301,
            "msg" : "Invalid Password"
        }

        num_token = count_Tokens(username)

        if num_token <= 0:
            retJson = {
            "status" : 303,
            "msg" : "Out of tockens"
        }

        nlp = spacy.load('en_core_web_sm-2.0.0.tar.gz')

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        retJson = {
            "status" : 200,
            "similarity" : ratio,
            "msg" : "similarity tested successfully"
        }

        current_tokens = count_Tokens(username)

        users.update({
            "Username" : username
        },{
            "Tokens" : current_tokens - 1
        })

        return jsonify(retJson)

        



