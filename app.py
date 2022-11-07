from flask import Flask, Response, request
from dotenv import load_dotenv
from controllers.UserCtr import register, send_email
from controllers.BankCtr import get_users, get_banklist, create
from flask_cors import CORS # remove for deploy
from utils.connection import connectMongo
import sys

app = Flask(__name__)
CORS(app) # remove for deploy

db = connectMongo()

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

# User Routes

@app.route("/register", methods=['POST'])
def register_route():
    try:
        register(request.json, db)
    
    except FileExistsError:
        return Response("Email Already Registered", status=400,  mimetype='application/json')

    except:
        return Response("Unknown Error", status=400,  mimetype='application/json')

    return Response("Success", status=200,  mimetype='application/json')

@app.route("/login", methods=['GET'])
def login_route():
    # GET JWT
    # repsond with JWT
    return Response("Success", status=200,  mimetype='application/json')

@app.route("/changepass", methods=['POST'])
def changepass_route():
    try:
        change_pass(request.json, db)
    
    except FileNotFoundError:
        print("No associated email")
        return Response("Email Not Found", status=400,  mimetype='application/json')

@app.route("/sendemail", methods=['POST'])
def sendemail_route():
    try:
        send_email(request.json, db)
    except:
        print("Error")
        return Response("Error", status=400,  mimetype='application/json')
    return Response("Success", status=200,  mimetype='application/json')

# Bank Routes

@app.route("/bank/getusers", methods=['GET'])
def getusers_route():
    return Response(get_users(db), status=200,  mimetype='application/json')

@app.route("/bank/getbanklist", methods=['GET'])
def getbanklist_route():
    return Response(get_banklist(db), status=200,  mimetype='application/json')

@app.route("/bank/create", methods=['POST'])
def create_route():
    try:
        create(request.json["data"], db)

    except ConnectionRefusedError:
        print("Could not connect with Inverite")
        return Response("Connection Error", status=400,  mimetype='application/json')
    
    except:
        print("Unknown Error")
        print(sys.exc_info(), "occurred.")
        return Response("Unknown Error", status=400,  mimetype='application/json')
    
    return Response("Success", status=200,  mimetype='application/json')

