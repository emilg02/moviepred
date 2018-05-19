import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import json
from django.http import HttpResponse
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
    data = pd.read_csv(cwd + "/movie/core/movies_new.csv")
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


