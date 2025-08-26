from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report
import numpy as np
import pickle

def init_Linear_Model(dt):
    # Split the data into features (X) and target (y)
    X = dt.drop(columns="job_level")
    y = dt['job_level']

    # Split the data into training and test sets (70% training, 30% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) 

    # Initialize and train the Linear model
    rf = LinearRegression()
    rf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf.predict(X_test)
    print("Score is ", f'{rf.score(X_test, y_test):.2%}')
    
    # Evaluate the model
    y_pred = y_pred.round()
    confusion = confusion_matrix(y_test, y_pred)
    print(y_pred)
    print(confusion)
    score = accuracy_score(y_test, y_pred)
    print(score)
    report = classification_report(y_test, y_pred, output_dict=True)
    report_file = open("static/reports/linear_report.txt", "w")
    report_file.write(str(report["macro avg"]["precision"]) + "\n")
    report_file.write(str(report["macro avg"]["recall"]) + "\n")
    report_file.write(str(report["macro avg"]["f1-score"]))
    report_file.close()

#link to the pickle file to display it on the website
    
    pickle_file = open("static/models/linear_pickle", "wb")
    pickle.dump(rf, pickle_file)
    pickle_file.close()