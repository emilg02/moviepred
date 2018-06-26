import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import json
from django.shortcuts import render, redirect
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from django.http import HttpResponse
import random
import numpy.ma as ma
import os

def calculate(request):
    movie = request.GET['movie']
    popularity = request.GET['popularity']
    vote_count = request.GET['vote_count']
    vote_average = request.GET['vote_average']
    budget = request.GET['budget']
    print (popularity)
    print (vote_count)
    print (vote_average)
    print (budget)
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
    model = forward_selected(train, columns,'revenue')

    model_param = model.params
    # print(model.summary())
    test_predict = model.predict(test)
    res = model.predict(pd.DataFrame({'popularity': [float(popularity)], 'vote_average': [float(vote_average)], 'vote_count': [int(vote_count)], 'budget': [int(budget)]}))
    return HttpResponse(json.dumps(res[0]), content_type="application/json")


def forward_selected(data, columns, response):
    remaining = columns
    selected = []
    current_score, best_new_score = 10000000, 10000000
    score_aic = []
    variable_added = []
    step = 2
    while (remaining and current_score == best_new_score and step > 0):
        scores_with_candidates = []
        for candidate in remaining:
            formula = "{} ~ {}".format(response, ' + '.join(selected + [candidate]))
            #print (formula)
            score = smf.ols(formula, data).fit().aic
            scores_with_candidates.append((score, candidate))
        scores_with_candidates.sort()
        best_new_score, best_candidate = scores_with_candidates.pop(0)
        if current_score > best_new_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            score_aic.append(best_new_score)
            variable_added.append(best_candidate)
            current_score = best_new_score
        step = step - 1
    formula = "{} ~ {}".format(response, ' + '.join(selected))
    model = smf.ols(formula, data).fit()

    return model


def linearModel(request):
    cwd = os.getcwd()
    Dataset = pd.read_csv(cwd + "/movie/data/movies_new.csv")
    #Train = pd.read_csv(cwd + "/movie/data/LinearTrainingSet.csv")
    # print df.head()

    #We split our dataset into training and testing sets
    Train, Test = train_test_split(Dataset, test_size=0.3, shuffle=False)

    #We select the relevant columns for the prediction
    data_Test = Test[['vote_average', 'budget', 'revenue']]
    data_Train = Train[['vote_average', 'budget', 'revenue']]

    x_Train = data_Train[['vote_average', 'budget']].values.reshape(-1, 2)
    y_Train = data_Train['revenue']

    x_Test = data_Test[['vote_average', 'budget']].values.reshape(-1, 2)
    y_Test = data_Test['revenue']
    title = Test[['title']]


    #Calculate Linear regression
    ols = linear_model.LinearRegression()
    model = ols.fit(x_Train, y_Train)
    output = model.predict(x_Test)
    output = np.rint(output)

    #Merge all
    resultDataframe = pd.DataFrame()
    resultDataframe = title
    resultDataframe['output'] = output
    resultDataframe['revenue'] = y_Test

    #The formula to calculate the error : MPE = ((Actual – Forecast) / Actual) x 100)
    forecast = pd.DataFrame()
    forecast['percent'] = ((resultDataframe['revenue'] - resultDataframe['output']) / resultDataframe['revenue']) * 100
    resultDataframe['percent'] = forecast.astype(int)

    #Convert dataframe to JSON file
    resultDataframe = resultDataframe.iloc[800:]

    resultDataframe = resultDataframe.drop(resultDataframe[resultDataframe.percent > 200].index)
    resultDataframe = resultDataframe.drop(resultDataframe[resultDataframe.percent < -200].index)
    resultDataframe = resultDataframe.sample(n=10)
    output = resultDataframe.to_json(orient='records')
    return HttpResponse(output, content_type="application/json")
