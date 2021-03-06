import numpy as np
import pandas as pd
from django.http import HttpResponse
import io
import movie.core.regression as reg
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn import linear_model
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split

def plot3d(request):
    cwd = os.getcwd()
    print(cwd)
    data = pd.read_csv(cwd + "/movie/data/movies_new.csv")
    data = data[:-3000]

    #Create train dataframes
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]
    X_train = data.iloc[:, 2:6]
    Y_train = data.iloc[:, 6]
    columns = list(X_train.columns.values)
    X_train.columns = columns
    train = pd.concat([X_train, Y_train], axis=1)

    #Create test dataframes
    X_test = test.iloc[:, 2:6]
    Y_test = test.iloc[:, 6]
    columns_test = list(X_test.columns.values)
    X_test.columns = columns_test
    test = pd.concat([X_test, Y_test], axis=1)

    #Creating the features concatenation
    features = "+".join(columns)

    ##Creating Null and Full formula
    null = 'revenue ~'
    full = 'revenue ~' + features
    model = reg.forward_selected(train, columns,'revenue')




    fit = model

    fit.summary()

    fig3d = plt.figure()
    ax = fig3d.add_subplot(111, projection='3d')

    x_surf = np.arange(0, 14000, 2000)  # generate a mesh
    y_surf = np.arange(0, 400000000, 10000000)
    x_surf, y_surf = np.meshgrid(x_surf, y_surf)

    exog = pd.core.frame.DataFrame({'vote_count': x_surf.ravel(), 'budget': y_surf.ravel()})
    out = fit.predict(exog=exog)

    ax.plot_surface(x_surf, y_surf,
                    out.values.reshape(x_surf.shape),
                    rstride=1,
                    cstride=1,
                    color='None',
                    alpha=0.4)

    ax.scatter(data['vote_count'], data['budget'], data['revenue'],
               c='blue',
               marker='o',
               alpha=1)

    ax.set_xlabel('vote_count')
    ax.set_ylabel('budget')
    ax.set_zlabel('revenue')

    canvas=FigureCanvas(fig3d)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig3d)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def plot2d(request):
    type = request.GET['type']
    print ("type is")
    print (type)
    # read data
    cwd = os.getcwd()
    data = pd.read_csv(cwd + "/movie/data/movies_new.csv")
    data = pd.DataFrame(data, columns=[type, 'revenue'])
    data = data[:-3000]

    x_values = data[type].values[:, np.newaxis]
    y_values = data['revenue'].values[:, np.newaxis]

    body_reg = linear_model.LinearRegression()
    body_reg.fit(x_values, y_values)
    prediction = body_reg.predict(np.sort(x_values, axis=0))

    fig = plt.figure()
    plt.scatter(x_values, y_values)
    plt.plot(np.sort(x_values, axis=0), prediction)
    plt.xlabel(type)
    plt.ylabel('revenue')
    canvas=FigureCanvas(fig)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def plotsvm(request):
    cwd = os.getcwd()
    df = pd.read_csv(cwd + "/movie/data/class.csv")
    df =df.dropna()

    X=df
    y=X['revenue_class']
    X = df[['vote_count','budget']]

    scaler=StandardScaler()
    X = scaler.fit_transform(X)
    y = np.array(y).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state =190)


    ### SVM
    clf = svm.SVC()
    clf.set_params(C=5)
    clf.fit(X_train, y_train)
    clf.predict(X_test)



    plot_decision_regions(X=X,
                          y=y,
                          clf=clf,
                          legend=2)

    # Update plot object with X/Y axis labels and Figure Title
    plt.xlabel(X[0], size=14)
    plt.ylabel(X[1], size=14)
    plt.title('SVM Decision Region Boundary', size=16)
    plt.xlabel('vote_count')
    plt.ylabel('budget')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


