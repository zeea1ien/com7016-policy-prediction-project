import pymongo

# Establish a connection to the MongoDB server
def connect_to_mongodb():
    try:
        mongodb = pymongo.MongoClient("mongodb://localhost:27017")
        print("Connected to MongoDB successfully!")
        return mongodb
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

# Function to insert data into MongoDB
def insert_data(data, mongodb):
    try:
        mydatabase = mongodb["EmployeeConn"]
        user_collection = mydatabase["EmployeeDB"]
        user_collection.insert_one(data)
        print("Data inserted successfully!")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

#Get Patient Data
def find_data(mongodb, search=None):
    data = []
    mydatabase = mongodb["EmployeeConn"]
    user_collection = mydatabase["EmployeeDB"]
    if search is not None:
        #If a search has been given, do that search.
        for patient in user_collection.find(search):
            patient.pop("_id")
            data.append(patient)
    else:
        #If a search has not been given, get ALL data from database
        for patient in user_collection.find():
            patient.pop("_id")
            data.append(patient)
    return data

#Delete Patient Data
def delete_patient(what_to_delete, mongodb):
    mydatabase = mongodb["EmployeeConn"]
    user_collection = mydatabase["EmployeeDB"]
    user_collection.delete_many(what_to_delete) #