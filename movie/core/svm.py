
import numpy as np
import pandas as pd
import sklearn
import os

from django.http import HttpResponse
from sklearn import tree
from pandas import *
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt

def classifier(row):
    if row["revenue"] <= 500000:
         return 1
    elif row["revenue"] > 500000 and row["revenue"] <= 1000000:
        return 2
    elif row["revenue"] > 1000000 and row["revenue"] <= 40000000:
        return 3
    elif row["revenue"] > 40000000 and row["revenue"] <= 150000000:
        return 4
    else:
        return 5

#Implementing SVM model
def svmModel(request):
    cwd = os.getcwd()

    df = pd.read_csv(cwd + "/movie/data/class.csv")
    df = df.dropna()

    # classify movies into 5 categories
    X = df
    y = X['revenue_class']
    X = df[['title','vote_count','budget']]
    y = np.array(y).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=190)
    title = X_test[['title']]
    X_train = X_train.drop(['title'], axis = 1)
    X_test =  X_test.drop(['title'], axis = 1)

    ### SVM
    clf = svm.SVC()
    clf.set_params(C=5)
    clf.fit(X_train, y_train)
    clf.predict(X_test)
    output = clf.predict(X_test)
    output = np.rint(output)

    #Merge all
    resultDataframe = title
    resultDataframe['output'] = output
    resultDataframe['revenue'] = y_test


    #Convert dataframe to JSON file
    resultDataframe = resultDataframe.sample(n=20)
    output = resultDataframe.to_json(orient='records')

    #return render(request, 'comparison.html', {'output': output})
    return HttpResponse(output, content_type="application/json")

