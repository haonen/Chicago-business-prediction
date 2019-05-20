'''
Aggreate the crime data by year and type 
'''

import data_loader as lo
import pandas as pd
import util as ut
import logging
import sys
import numpy as np
import argparse
import os
import sys
import pdb

logger = logging.getLogger('aggreate')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('./log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

def process(args):
    filename = args.filename
    df =  pd.read_csv(filename)
    res = df.groupby(['primary_type','zip']).count().reset_index().drop_duplicates(['primary_type','zip'])
    res = res[['primary_type','zip','block']]
    res['year'] = args.year
    res.rename(columns = {'block':'count'},inplace=True)
    res.to_csv(str(args.year) + '_res.csv')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pass file and year')
    parser.add_argument('--file', dest='filename', type=str, default='2013.csv')
    parser.add_argument('--year', dest ='year', type=int, default =2013)
    args = parser.parse_args()
    process(args)
                                                                                    
