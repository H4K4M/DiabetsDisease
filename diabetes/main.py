import numpy as np
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm

from csv import writer
def append_list_as_row(filename, list_of_elem):
    # Open file in append mode
    with open('diabetes.csv', 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

diabetes_dataset = pd.read_csv('D:\Documents(D)\diabetes\diabetes.csv')
# separating the data and labels
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']
scaler = StandardScaler()
scaler.fit(X)
standardized_data = scaler.transform(X)
X = standardized_data
Y = diabetes_dataset['Outcome']
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)
classifier = svm.SVC(kernel='linear')
#training the support vector Machine Classifier
classifier.fit(X_train, Y_train)

filename = 'diabetes_trained_model.sav'
pickle.dump(classifier,open(filename,'wb'))

trained_model = pickle.load(open('D:\Documents(D)\diabetes\diabetes_trained_model.sav','rb'))
# loading the diabetes dataset to a pandas DataFrame

# input_data = [1,93,70,31,0,30.4,0.315,23]
# #input_data = [6,148,72,35,0,33.6,0.627,50]

# # changing the input_data to numpy array
# input_data_as_numpy_array = np.asarray(input_data)

# # reshape the array as we are predicting for one instance
# input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
# print(input_data_reshaped)
# # standardize the input data
# std_data = scaler.transform(input_data_reshaped)
# print(std_data)
# prediction = trained_model.predict(std_data)
# print(prediction)
# if (prediction[0] == 0):
#   print('The person is not diabetic')
# else:
#   print('The person is diabetic')

# #input_list = input_data_as_numpy_array.tolist()
# input_list = input_data
# input_list.append(prediction[0])


# #append_list_as_row('diabetes.csv', input_list)
# # Open file in append mode
# with open('diabetes.csv', 'a+', newline='') as write_obj:
#     # Create a writer object from csv module
#     csv_writer = writer(write_obj)
#     # Add contents of list as last row in the csv file
#     csv_writer.writerow(input_list)


import unittest
class TestResult(unittest.TestCase):
    

    
    def test_two(self):
        self.assertTrue(is_sick(6,148,72,35,0,33.6,0.627,50))

    
    
   
def is_sick(Pregnancies, Glucose, BloodPressure,	SkinThickness,	Insulin,	BMI,	DiabetesPedigreeFunction,	Age):
  input_data = [Pregnancies, Glucose, BloodPressure,	SkinThickness,	Insulin,	BMI,	DiabetesPedigreeFunction,	Age]
  input_data_as_numpy_array = np.asarray(input_data)

  # reshape the array as we are predicting for one instance
  input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
  print(input_data_reshaped)
  # standardize the input data
  std_data = scaler.transform(input_data_reshaped)
  print(std_data)
  prediction = trained_model.predict(std_data)
  print(prediction)
  if (prediction[0] == 0):
    return False
  else:
    return True


unittest.main()