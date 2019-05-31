'''
feature generator for the pipeline
Pengwei
'''
import pandas as pd
import logging
import sys
import numpy as np
import argparse
import os
import pdb

logger = logging.getLogger('generating features from the data')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('../log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

def binnize(df, ):
    '''
    model factory generate the next aviable model 
    from the config file
    
    Input: 
        config: dict from , value as the parameters
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


def 
