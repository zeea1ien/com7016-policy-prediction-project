from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report
import numpy as np
import pickle

def init_Random_Forest_Model(dt):
    # Split the data into features (X) and target (y)
    X = dt.drop(columns="job_level")
    y = dt['job_level']

    # Split the data into training and test sets (70% training, 30% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) 

    # Initialize and train the Random Forest model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf.predict(X_test)
    print("Score is ", f'{rf.score(X_test, y_test):.2%}')
    
    # Evaluates the model and creates the graphs
    confusion = confusion_matrix(y_test, y_pred)
    print(confusion)
    score = accuracy_score(y_test, y_pred)
    print(score)
    report = classification_report(y_test, y_pred, output_dict=True)
    report_file = open("static/reports/random_report.txt", "w")
    report_file.write(str(report["macro avg"]["precision"]) + "\n")
    report_file.write(str(report["macro avg"]["recall"]) + "\n")
    report_file.write(str(report["macro avg"]["f1-score"]))
    report_file.close()

#displays it in results
    pickle_file = open("static/models/random_pickle", "wb")
    pickle.dump(rf, pickle_file)
    pickle_file.close()