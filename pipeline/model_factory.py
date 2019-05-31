'''
Model factory for the pipeline
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
from itertools import product
import logging
import sys
import numpy as np
import argparse
import os
import pdb

logger = logging.getLogger('generating models')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('../log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


def get_models(file):
    '''
    model factory generate the next aviable model 
    from the config file
    
    Input: 
        file:  the yml file that used to generate the models
    Return:
        A iterable of models
    ''' 
    logger.info('begin to generate the models')
    with open(file) as config_file:
        config = yaml.safe_load(config_file)['models']
        for (name, params) in config.items():
            pdb.set_trace()
            constructor = globals()[name]
            models = [constructor(**dict(zip(params.keys(),vals))) for vals in product(*params.values())]
            for model in models:
                logger.info('{} is delivering out'.format(model))
                yield model
