from sklearn.model_selection import ParameterGrid
import datetime
import pandas as pd
from evaluation import *


def run_models(models_list, clfs, grid, X_train, X_test, y_train, y_test, threshold):
    """
    models_list: (list of str) names of models to run
    clfs: (dict) base models
    grid: (dict of dict) parameter grid of models
    X_train: (df) train data set
    X_test: (df) test data set

    """
    # create the empty data frame
    col_list = ['model_name', 'parameters', 'baseline', 'accuracy',
                'f1', 'auc_roc', 'precision_1%', 'precision_2%',
                'precision_5%', 'precision_10%', 'precision_20%', 'precision_30%',
                'precision_50%', 'recall_1%', 'recall_2%', 'recall_5%',
                'recall_10%', 'recall_20%','recall_30%', 'recall_50%']
    results_df = pd.DataFrame(columns=col_list)
    
    for index, clf in enumerate([clfs[x] for x in models_list]):
        parameter_values = grid[models_list[index]]
        for params in ParameterGrid(parameter_values):
            try:
                print("Running {} ...".format(models_list[index]))
                clf.set_params(**params)
                if models_list[index] == 'Support Vector Machine':
                    y_pred_probs = clf.fit(X_train, y_train).decision_function(X_test)
                else:
                    y_pred_probs = clf.fit(X_train, y_train).predict_proba(X_test)[:, 1]
                
                if models_list[index] == "Decision Tree" or models_list[index] == "Random Forest":
                    d = {'Features': X_train.columns, "Importance": clf.feature_importances_}
                    feature_importance = pd.DataFrame(data=d)
                    feature_importance = feature_importance.sort_values(by=['Importance'], ascending=False)
                    print(feature_importance.head())
                
                # Sort true y labels and predicted scores at the same time    
                y_pred_probs_sorted, y_test_sorted = zip(*sorted(zip(y_pred_probs, y_test), reverse=True))
                # Write the evaluation results into data frame
                results_df.loc[len(results_df)] = [models_list[index], params,
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 100),
                                                   compute_acc(y_test_sorted, y_pred_probs_sorted, threshold),
                                                   compute_f1(y_test_sorted, y_pred_probs_sorted, threshold),
                                                   compute_auc_roc(y_test_sorted, y_pred_probs_sorted, threshold),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 1),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 2),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 5),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 10),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 20),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 30),
                                                   precision_at_k(y_test_sorted, y_pred_probs_sorted, 50),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 1),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 2),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 5),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 10),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 20),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 30),
                                                   recall_at_k(y_test_sorted, y_pred_probs_sorted, 50)]

                graph_name_pr = './graphs/' + 'precision_recall_curve' + ": " + models_list[index] +\
                                 datetime.now().strftime("%m-%d-%Y, %H%M%S")
                plot_precision_recall_n(y_test, y_pred_probs, graph_name_pr, 'save')
                graph_name_roc = './graphs/' + 'roc_curve' + ": " + models_list[index] +\
                                 datetime.now().strftime("%m-%d-%Y, %H%M%S")
                plot_roc(graph_name_roc, y_pred_probs, y_test, 'save')
            except IndexError as e:
                print('Error:', e)
                continue
    return results_df



