
import numpy as np
import pandas as pd
import sklearn
import os
from sklearn import tree
from pandas import *
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
cwd = os.getcwd()
print(cwd)
#df = pd.read_csv(cwd + "/movie/data/movies_new.csv")
df = pd.read_csv("class.csv")
df =df.dropna()

#classify movies into 5 categories
#df["revenue_class"] = df.apply(classifier, axis=1)



X=df
y=X['revenue_class']
X = X.drop(['revenue_class'], axis = 1)
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

scaler=StandardScaler()
X = scaler.fit_transform(X)
y = np.array(y).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state =190)


# ## SVM

# In[9]:

from sklearn import svm

clf = svm.SVC()
clf.set_params(C=10)
clf.fit(X_train, y_train)
clf.predict(X_test)

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
prediction = clf.predict(X_test)
print(accuracy_score(y_test,prediction))


# ## Linear SVM

# In[10]:

clfLin = svm.SVC(kernel = 'linear')
clfLin.set_params(C=0.5)
clfLin.fit(X_train,y_train)
clfLin.predict(X_test)

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
prediction = clfLin.predict(X_test)
print(accuracy_score(y_test,prediction))



