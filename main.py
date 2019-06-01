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
from pipeline import *
import pdb

logger = logging.getLogger('generating models')
ch = logging.StreamHandler(sys.stdout)
#fh = logging.FileHandler('../log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
#fh.setFormatter(formatter)
logger.addHandler(ch)
#logger.addHandler(fh)
logger.setLevel(logging.INFO)


def run(args):
    logger.info("starting to run the pipeline")
    pdb.set_trace()
    config = args.config
    with open (config) as config_file:
        configs = yaml.safe_load(config_file)
    # 'input_file', 'roc_path', 'pr_path','out_path']
    io_dic = configs['io']
    x_cols = configs['x_cols']
    y_col = configs['y_col']
    time_col = configs['time_col']
    # 'start_year', 'end_year', 'update_period', 'test_period'
    time_dic = configs['time']
    percentage = configs['percentage']









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do a simple machine learning pipeline, load data, split the data, transform data, build models, run models, get the performace matix results')
    parser.add_argument('--config', dest='config', help='config file for this run', default ='./test_simple.yml')
    args = parser.parse_args()
    run(args)
