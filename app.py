from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
from SQLite_handler import *
from mongo_loader import *
from user import User
import os
import sqlite3
import pymongo
import random as R
import ast

users = {} #global dict to store users data

create_connection()
mongo_connection = connect_to_mongodb()
app = Flask(__name__)
app.secret_key = "ASecretButNotSoSecretKey"# secret key for secuirty- to protect user session data 
#mongodb = pymongo.MongoClient("mongodb://localhost:27017")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_fuser(id):
    user_info = user_check_confirmation(id)
    if len(user_info) <= 0:
        return None
    else:
        return User(user_info["id"], user_info["username"])
    

# Route for the homepage
@app.route('/')
def home():
    if current_user.is_authenticated is True:
        return render_template('home.html', user_data=find_data(mongo_connection, {"name": current_user.username}))
    else:
        return render_template('home.html', user_data=find_data(mongo_connection, {"name": None}))
#Signup
@app.route("/signup")
def signup():
    if current_user.is_authenticated is False:
        return render_template("register.html")
    else:
        return redirect("/")
    
@app.route("/login")
def login():
    if current_user.is_authenticated is False:
        return render_template("login.html")
    else:
        return redirect("/")
    
@app.route('/logout')
def logout():
    if current_user.is_authenticated is True:
        logout_user()
    return redirect('/')

@app.route("/loggingIn", methods=["POST"])
def loggingIn():
    if current_user.is_authenticated is False:
        user_dict = {}
        user_data = request.get_data()
        user_data = user_data.decode()
        user_data = user_data.split("&")
        user_dict["username"] = user_data[0].replace("username=", "")
        user_dict["password"] = user_data[1].replace("password=", "")
      
        if user_exists(user_dict["username"]) is True:
            login_user(User(user_getID(user_dict["username"]), user_dict["username"],))
            return redirect('/')
        else:
            return "User does not exist"
    else:
        return redirect("/")
    
# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    if current_user.is_authenticated is False:
        user_dict = {}
        user_data = request.get_data()
        user_data = user_data.decode()
        user_data = user_data.split("&")
        user_dict["username"] = user_data[0].replace("username=", "")
        user_dict["password"] = user_data[1].replace("password=", "")
        create_user(user_dict)
        return redirect('/')
    else:
        return redirect("/")

# Route to employee survey 
@app.route('/employee_form')
def employee_form():
    if current_user.is_authenticated:
        return render_template('employee_form.html')
    else:
        return redirect("/")
    
@app.route('/employee_form/submit', methods=['POST'])
def employee_form_process():
    if current_user.is_authenticated:
        employee_data = request.get_data()
        employee_data = employee_data.decode()
        employee_data = employee_data.split("&")
        for item in employee_data:
            item = item.split("=")
            if "+" in item[1]:
                item[1] = item[1].replace("+", " ")
            employee_data[item[0]] = item[1]
        employee_data["name"] = current_user.username
    return redirect('/')

@app.route('/view_patients')
def view_patients():
    # Retrieve patients from MongoDB
    return render_template('patients.html', mongo_patients=find_data(mongo_connection))

@app.route('/your_data')
def user_data():
    if current_user.is_authenticated is True:
        return render_template('profile.html', user_data=find_data(mongo_connection, {"name": current_user.username}))
    else:
         
        return redirect('/')

@app.route('/delete_data')
def delete_data():
    delete_patient({"name": current_user.username}, mongo_connection)
    return redirect('/')

@app.route('/delete_user')
def delete_user():
    if current_user.is_authenticated is True:
        username = current_user.username
        logout_user()
        user_delete(username)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)