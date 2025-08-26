import pandas as pd 
from RandomForest_Model import *
from Linear_Model import *

#creates the file maps 
def save_map(column_map, column_name):
    map_file = open("maps/" + column_name + "_map.txt", "w")
    counter = 0
    for item in column_map:
        if counter == 0:
            map_file.write(str(item))
        else:
            map_file.write("\n" + str(item))
        counter += 1
    map_file.close()

def map_column(dataset, column_name):
    row_counter = 0
    column_map = []
    for row in dataset[column_name]:
        if row not in column_map:
            column_map.append(row)
        dataset.loc[row_counter, column_name] = column_map.index(row)
        row_counter += 1
    save_map(column_map, column_name)
    return dataset

#loads the datasets 
df = pd.read_csv("Employee Satisfaction Index.csv", index_col=0)
cleaned_data = df.drop(columns={"emp_id", "location", "recruitment_type"}, index=1)
cleaned_data = cleaned_data.reset_index(drop=True)
cleaned_data = map_column(cleaned_data, "Dept")
cleaned_data = map_column(cleaned_data, "education")
cleaned_data.to_csv("Employee Satisfaction Index Cleaned.csv")
init_Random_Forest_Model(cleaned_data)
print("--------------------------------------------------------------------------")
init_Linear_Model(cleaned_data)
for column in cleaned_data:
    print(column)