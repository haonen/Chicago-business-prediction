'''
spliter the dataframe based on the time information.
'''
from collections import OrderedDict
from itertools import product
import logging
import sys
import numpy as np
import argparse
import os
import pdb

logger = logging.getLogger('generating models')
ch = logging.StreamHandler(sys.stdout)
#fh = logging.FileHandler('./log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
#fh.setFormatter(formatter)
logger.addHandler(ch)
#logger.addHandler(fh)
logger.setLevel(logging.INFO)


def get_models(config):
    '''
    model factory generate the next aviable model 
    from the config file
    
    Input: 
        config: OrdedDict with the key as the name of the model, value as the parameters 
    Return:
        A iterable of models
    ''' 
    logger.info('begin to generate the models')
    for (name, params) in config.items():
        constructor = globals()[name]
        models = [constructor(**dict(zip(params.keys(),vals))) for vals in product(*params.values())]
        for model in models:
            logger.info('{} is delivering out'.format(model))
            yield model

