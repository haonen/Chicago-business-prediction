from community_mean_imputer import *
from get_dummy import *
from modeling import*
from minmax_scaler import *


def wrap_up(X, y, min_year, max_year, loc_column, time_column, categorical_col, k, model_list, clfs, grid, threshold, save_path):
    '''

    :param X:
    :param y:
    :param min_year:
    :param max_year:
    :param loc_column:
    :param time_column:
    :param categorical_col:
    :param k:
    :param model_list:
    :param clfs:
    :param grid:
    :param threshold:
    :return:
    '''
    evaluation_results = []
    for year in range(min_year + 1, max_year - 3, 2):
        X_train = X[X['year'] <= year]
        X_test = X[(X['year'] == year + 3) | (X['year'] == year + 4)]
        y_train = y[X['year'] <= year]
        y_test = y[(X['year'] == year + 3) | (X['year'] == year + 4)]
        print(len(X_test), len(X_train))

        #imputation
        imputer = community_mean_imputer()
        X_train, X_test = imputer.filled_categorical(X_train, X_test, categorical_col)
        X_train = imputer.train_regional_mean(X_train, loc_column, time_column)
        X_test = imputer.transform_test(X_test, loc_column, time_column)
       

        # Drop year column
        X_train = X_train.drop(columns=[time_column])
        X_test = X_test.drop(columns=[time_column])
        
        #Scaling
        continuous_columns = list(set(X_train.columns) - set(categorical_col))
        X_train, X_test = min_max_transformation(X_train, X_test, continuous_columns)

        #get dummies
        for col in categorical_col:
            X_train, X_test = get_dummies(X_train, X_test, col, k)
        
        

        #run models
        df = run_models(model_list, clfs, grid, X_train, X_test, y_train, y_test, threshold, save_path)
        evaluation_results.append(df)

    return evaluation_results
