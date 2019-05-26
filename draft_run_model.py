from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.grid_search import ParameterGrid
from datetime import timedelta


def run_models(models_list, clfs, grid, X_train, X_test, y_train, y_test, threshold):
    """
    """
    # create the empty data frame
    col_list = ['model_name', 'parameters', 'baseline', 'accuarcy', 'f1', 'auc_roc',
                'precision_1%', 'precision_2%', 'precision_5%',
                'precision_10%', 'precision_20%', 'precision_30%',
                'precision_50%', 'recall_1%', 'recall_2%',
                'recall_5%', 'recall_10%', 'recall_20%','recall_30%', 'recall_50%' ]
    results_df =  pd.DataFrame(columns=col_list)
    
    for index,clf in enumerate([clfs[x] for x in models_list]):
        parameter_values = grid[models_list[index]]
        for params in ParameterGrid(parameter_values):
            try:
                print("Running {} ...".format(models_list[index]))
                clf.set_params(**params)
                if models_list[index] == 'Support Vector Machine':
                    y_pred_probs = clf.fit(X_train, y_train).decision_function(X_test)
                else:
                    y_pred_probs = clf.fit(X_train, y_train).predict_proba(X_test)[:,1]
                
                if models_list[index] == "Decision Tree" or models_list[index] == "Random Forest":
                    d = {'Features': X_train.columns, "Importance": clf.feature_importances_}
                    feature_importance = pd.DataFrame(data=d)
                    feature_importance = feature_importance.sort_values(by=['Importance'], ascending=False)
                    print(feature_importance.head())
                
                # Sort true y labels and predicted scores at the same time    
                y_pred_probs_sorted, y_test_sorted = zip(*sorted(zip(y_pred_probs, y_test), reverse=True))
                # Write the evaluation results into data frame
                results_df.loc[len(results_df)] = [models_list[index], params,
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted, 100),
                                                   compute_acc(y_test_sorted, y_pred_probs_sorted, threshold),                                                              compute_f1(y_test_sorted, y_pred_probs_sorted, threshold),
                                                   compute_auc_roc(y_test_sorted, y_pred_probs_sorted, threshold),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,1),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,2),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,5),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,10),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,20),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,30),
                                                   precision_at_k(y_test_sorted,y_pred_probs_sorted,50),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,1),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,2),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,5),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,10),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,20),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,30),
                                                   recall_at_k(y_test_sorted,y_pred_probs_sorted,50)]
                
                plot_precision_recall_n(y_test,y_pred_probs, clf, 'show')
            except IndexError as e:
                print('Error:',e)
                continue
    return results_df


def compute_acc(y_true, y_scores, k):
    '''
    Compute accuracy score based on threshold
    :param pred_scores: (np array) an array of predicted score
    :param threshold: (float) the threshold of labeling predicted results
    :param y_test: test set

    :return: (float) an accuracy score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)

    return accuracy_score(y_true_sorted, preds_at_k)


def compute_f1(y_true, y_scores, k):
    '''
    Compute f1 score based on threshold
    :param pred_scores: (np array) an array of predicted score
    :param threshold: (float) the threshold of labeling predicted results
    :param y_test: test set

    :return: (float) an f1 score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)

    return f1_score(y_true_sorted, preds_at_k)

def compute_auc_roc(y_true, y_scores, k):
    '''
    Compute area under Receiver Operator Characteristic Curve
    :param pred_scores: (np array) an array of predicted score
    :param threshold: (float) the threshold of labeling predicted results
    :param y_test: test set

    :return: (float) an auc_roc score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)

    return roc_auc_score(y_true_sorted, preds_at_k)


def compute_auc(pred_scores, true_labels):
    '''
    Compute auc score
    :param pred_scores: an array of predicted scores
    :param true_labels: an array of true labels

    :return: area under curve score
    '''
    fpr, tpr, thresholds = roc_curve(true_labels, pred_scores, pos_label=2)
    return auc(fpr, tpr)


# The following functions are referenced from:
# https://github.com/rayidghani/magicloops/blob/master/mlfunctions.py

def joint_sort_descending(l1, l2):
    '''
    Sort two arrays together
    :param l1:  numpy array
    :param l2:  numpy array

    :return: two sorted arrays
    '''
    idx = np.argsort(l1)[::-1]
    return l1[idx], l2[idx]


def generate_binary_at_k(y_scores, k):
    '''
    predict labels based on thresholds
    :param y_scores: the predicted scores
    :param k: (int or float) threshold

    :return: predicted labels
    '''
    cutoff_index = int(len(y_scores) * (k / 100.0))
    predictions_binary = [1 if x < cutoff_index else 0 for x in range(len(y_scores))]
    return predictions_binary


def precision_at_k(y_true, y_scores, k):
    '''
    Compute precision based on threshold (percentage)
    :param y_true: the true labels
    :param y_scores: the predicted labels
    :param k: (int or float) the threshold

    :return: (float) precision score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)
    return precision_score(y_true_sorted, preds_at_k)


def recall_at_k(y_true, y_scores, k):
    '''
    Compute recall based on threshold (percentage)
    :param y_true: the true labels
    :param y_scores: the predicted labels
    :param k: (int or float) the threshold

    :return: (float) recall score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)
    return recall_score(y_true_sorted, preds_at_k)


def plot_precision_recall_n(y_true, y_prob, model_name, output_type):
    '''
    Plot precision and recall at different percent of population
    :param y_true: the true labels
    :param y_prob: the predicted labels
    :param model_name: the name of the model
    :param output_type: (str) 'save' or 'show'

    :return: No returns but a plot
    '''
    y_score = y_prob
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_true, y_score)
    precision_curve = precision_curve[:-1]
    recall_curve = recall_curve[:-1]
    pct_above_per_thresh = []
    number_scored = len(y_score)
    for value in pr_thresholds:
        num_above_thresh = len(y_score[y_score >= value])
        pct_above_thresh = num_above_thresh / float(number_scored)
        pct_above_per_thresh.append(pct_above_thresh)
    pct_above_per_thresh = np.array(pct_above_per_thresh)

    plt.clf()
    fig, ax1 = plt.subplots()
    ax1.plot(pct_above_per_thresh, precision_curve, 'b')
    ax1.set_xlabel('percent of population')
    ax1.set_ylabel('precision', color='b')
    ax2 = ax1.twinx()
    ax2.plot(pct_above_per_thresh, recall_curve, 'r')
    ax2.set_ylabel('recall', color='r')
    ax1.set_ylim([0, 1])
    ax1.set_ylim([0, 1])
    ax2.set_xlim([0, 1])

    name = model_name
    plt.title(name)
    if (output_type == 'save'):
        plt.savefig(name)
    elif (output_type == 'show'):
        plt.show()
    else:
        plt.show()
