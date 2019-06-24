## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize, MinMaxScaler
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 0.3, shuffle=True, random_state=random_state )


# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
regr = LinearRegression()
regr.fit(x_train, y_train)

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX
y_predict_test = regr.predict(x_test)
y_predict_train = regr.predict(x_train)
accuracy_test = accuracy_score(y_test, y_predict_test.round())
accuracy_train = accuracy_score(y_train, y_predict_train.round())
print("LR test score: %.2f"%accuracy_test)
print("LR training score: %.2f"%accuracy_train)

# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
y_predict_test = rfc.predict(x_test)
y_predict_train = rfc.predict(x_train)
accuracy_test = accuracy_score(y_test, y_predict_test.round())
accuracy_train = accuracy_score(y_train, y_predict_train.round())
print("RFC test score: %.2f"%accuracy_test)
print("RFC training score: %.2f"%accuracy_train)

# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
importances = rfc.feature_importances_
indices =np.argsort(t)[::-1]
for f in range(x_train.shape[1]):
	print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

#X7
#X5
# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
param_grid = {
    'n_estimators': [100,200,300],
    'max_depth':[50,100,150]
}

cv_rfc = GridSearchCV(rfc, param_grid=param_grid , cv=10)
cv_rfc = cv_rfc.fit(MinMaxScaler().fit_transform(x_train), y_train)
print(cv_rfc.best_params_)
print(cv_rfc.best_score_)

# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
svc = SVC()
svc.fit(x_train, y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
y_predict_test = svc.predict(x_test)
y_predict_train = svc.predict(x_train)
accuracy_test = accuracy_score(y_test, y_predict_test.round())
accuracy_train = accuracy_score(y_train, y_predict_train.round())
print("SVC test score: %.2f"%accuracy_test)
print("SVC training score: %.2f"%accuracy_train)

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
param_grid = {
    'kernel':('rbf', 'linear'),
    'C':[0.001, 0.01, 0.1]
}

cv_svc = GridSearchCV(svc, param_grid=param_grid , cv=10)
cv_svc = cv_svc.fit(MinMaxScaler().fit_transform(x_train), y_train)
print(cv_svc.best_params_)
print(cv_svc.cv_results_)
print(cv_svc.cv_results_)


# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX

pca = PCA(n_components=10, svd_solver='full')
pca.fit(data)

print(pca.explained_variance_ratio_)  
print(pca.singular_values_)  




