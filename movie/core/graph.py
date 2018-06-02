import numpy as np
import pandas as pd
from django.http import HttpResponse
import io
import movie.core.regression as reg
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def plot3d(request):
    cwd = os.getcwd()
    print(cwd)
    data = pd.read_csv(cwd + "/movie/data/movies_new.csv")
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

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_surf = np.arange(0, 350, 20)  # generate a mesh
    y_surf = np.arange(0, 60, 4)
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

    canvas=FigureCanvas(fig)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


