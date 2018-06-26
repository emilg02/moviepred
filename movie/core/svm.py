
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
# cwd = os.getcwd()
# print(cwd)
# #df = pd.read_csv(cwd + "/movie/data/movies_new.csv")
# df = pd.read_csv("class.csv")
# df =df.dropna()
#
# #classify movies into 5 categories
# #df["revenue_class"] = df.apply(classifier, axis=1)
#
# X=df
# y=X['revenue_class']
# X = X.drop(['revenue_class'], axis = 1)
# X = X.drop(['popularity'], axis=1)
# X = X.drop(['vote_average'], axis=1)
# scaler=StandardScaler()
# X = scaler.fit_transform(X)
# y = np.array(y).astype(int)
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state =190)
#
#
# ### SVM
# clf = svm.SVC()
# clf.set_params(C=5)
# clf.fit(X_train, y_train)
# clf.predict(X_test)
# prediction = clf.predict(X_test)
# print(accuracy_score(y_test,prediction))
#
#
# ### Linear SVM
# clfLin = svm.SVC(kernel = 'linear')
# clfLin.set_params(C=0.5)
# clfLin.fit(X_train,y_train)
# clfLin.predict(X_test)
# prediction = clfLin.predict(X_test)
# print(accuracy_score(y_test,prediction))
#
#
#
#
#
# plot_decision_regions(X=X,
#                       y=y,
#                       clf=clf,
#                       legend=2)
#
# # Update plot object with X/Y axis labels and Figure Title
# plt.xlabel(X[0], size=14)
# plt.ylabel(X[1], size=14)
# plt.title('SVM Decision Region Boundary', size=16)
# plt.show()

def svmModel(request):
    cwd = os.getcwd()
    print(cwd)
    # df = pd.read_csv(cwd + "/movie/data/movies_new.csv")
    df = pd.read_csv(cwd + "/movie/data/class.csv")
    df = df.dropna()

    # classify movies into 5 categories
    # df["revenue_class"] = df.apply(classifier, axis=1)

    X = df
    y = X['revenue_class']
    X = df[['title','vote_count','budget']]
    #scaler = StandardScaler()
    #X = scaler.fit_transform(X)
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
    print(output)


    #Merge all
    resultDataframe = title
    resultDataframe['output'] = output
    resultDataframe['revenue'] = y_test


    #Convert dataframe to JSON file
    resultDataframe = resultDataframe.sample(n=20)
    output = resultDataframe.to_json(orient='records')

    #return render(request, 'comparison.html', {'output': output})
    return HttpResponse(output, content_type="application/json")

