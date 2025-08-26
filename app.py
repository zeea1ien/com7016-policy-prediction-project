from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
from SQLite_handler import *
from mongo_loader import *
from user import User
import random as R
import pandas as pd
import pickle



users = {} #global dict to store users data

create_connection()
mongodb = connect_to_mongodb()
app = Flask(__name__)
app.secret_key = "ASecretButNotSoSecretKey"# secret key for secuirty- to protect user session data 
mongodb = connect_to_mongodb()

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
        return render_template('home.html', user_data=find_data(mongodb, {"name": current_user.username}))
    else:
        return render_template('home.html', user_data=find_data(mongodb, {"name": None}))
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
    
#route to chatbot page 
@app.route('/chatbot')
def chatbot():
    if current_user.is_authenticated:
        return render_template('chatbot.html')
    else:
        return redirect("/")
    
@app.route('/employee_form/submit', methods=['POST'])
def employee_form_process():
    if current_user.is_authenticated:
        employee_data = request.get_data()
        employee_data = employee_data.decode()
        employee_data = employee_data.split("&")
        employee_data_dict = {}
        prediction = 0
        model = "Linear"
        for item in employee_data:
            item = item.split("=")
            print(item[0], item[1], flush=True)
            employee_data_dict[item[0]] = [int(item[1])]
        if employee_data_dict["model_selection"] == [0]:
            employee_data_panda = pd.DataFrame(employee_data_dict)
            employee_data_panda = employee_data_panda.drop(columns={"model_selection", "job_level"})
            employee_data_panda = employee_data_panda[["age", "Dept", "education", "rating", "onsite", "awards", "certifications", "salary", "satisfied"]]
            model_file = open("./static/models/linear_pickle", "rb")
            model = pickle.load(model_file)
            model_file.close()
            prediction = model.predict(X=employee_data_panda)
        else:
            employee_data_panda = pd.DataFrame(employee_data_dict)
            employee_data_panda = employee_data_panda.drop(columns={"model_selection", "job_level"})
            employee_data_panda = employee_data_panda[["age", "Dept", "education", "rating", "onsite", "awards", "certifications", "salary", "satisfied"]]
            model_file = open("./static/models/random_pickle", "rb")
            model = pickle.load(model_file)
            model_file.close()
            prediction = model.predict(X=employee_data_panda)
            model = "Random Forest"
        print(prediction)
        return render_template("result.html", result=prediction, model=model)
    else:
        return redirect("/")

@app.route('/view_employee')
def view_employees():
    # Retrieve patients from MongoDB
    return render_template('patients.html', mongo_patients=find_data(mongodb))

@app.route('/your_data')
def user_data():
    if current_user.is_authenticated is True:
        return render_template('profile.html', user_data=find_data(mongodb, {"name": current_user.username}))
    else:
         
        return redirect('/')

@app.route('/delete_data')
def delete_data():
    delete_employees({"name": current_user.username}, mongodb)
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