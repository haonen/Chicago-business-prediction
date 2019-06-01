'''
Main function for the pipeline
'''
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import yaml
from collections import OrderedDict
from itertools import product
import logging
import sys
import numpy as np
import argparse
import os
from pipeline import model_factory
from pipeline import evaluation
import transformer
import pandas as pd
import pdb

logger = logging.getLogger('main function')
ch = logging.StreamHandler(sys.stdout)
#fh = logging.FileHandler('../log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
#fh.setFormatter(formatter)
logger.addHandler(ch)
#logger.addHandler(fh)
logger.setLevel(logging.INFO)


def run(config):
    logger.info("starting to run the pipeline")
    #pdb.set_trace()
    #config = args.config
    with open (config) as config_file:
        configs = yaml.safe_load(config_file)
    #'input_file', 'roc_path', 'pr_path','out_path'

    df = pd.read_csv(configs['io']['input_path'])
    cols_config = configs['cols']
    time_config = configs['time']
    trans_configs = configs['transform']
    model_configs = configs['models']
    for data in split(cols_config, time_config, df):
        X_train, X_test, Y_train, Y_test = data
        X_train, X_test = transformer.transform(trans_configs, X_train, X_test)
        for model in model_factory.get_models(model_configs):
            logger.info('start to run the model {}'.format(model))
            model.fit(X_train, Y_train)
            model.predict_proba(X_test)[:, 1]
        

def split(cols_config, time_config, df):
    logger.info('starging to split the dataframe')
    X = df[cols_config['x_cols']]
    y = df[cols_config['y_col']]
    min_year = time_config['start_year']
    max_year = time_config['end_year']
    for year in range(min_year + 1, max_year - 3, 2):
        X_train = X[X['year'] <= year]
        X_test = X[(X['year'] == year + 3) | (X['year'] == year + 4)]
        y_train = y[X['year'] <= year].values
        y_test = y[(X['year'] == year + 3) | (X['year'] == year + 4)].values
        logger.info('delivering data to pipeline')
        yield X_train, X_test, y_train, y_test


def get_matrix():
    



    pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do a simple machine learning pipeline, load data, split the data, transform data, build models, run models, get the performace matix results')
    parser.add_argument('--config', dest='config', help='config file for this run', default ='./test_simple.yml')
    args = parser.parse_args()
    run(args)



