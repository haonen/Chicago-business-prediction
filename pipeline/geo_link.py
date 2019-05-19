'''

Link the any data with the colum of latitude and longitude
with two levels of geo data, one is zip code level, the other
is the neighborhood level
'''

import data_loader as lo
import pandas as pd
import util as ut
import logging
import sys
import numpy as np
import csv
import pdb

logger = logging.getLogger('merging')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('./log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

ZIPCODES_ID = 'unjd-c2ca'
NEIGHS_ID = 'y6yq-dbs2'


def drop(df, long_col, lat_col):
    '''
    drop rows where the longitude or latitude is null
    '''
    logger.info("dropping the longitude and latitude nulls")
    temp = df.shape[0]
    df = df[df[long_col].notnull()]
    df = df[df[lat_col].notnull()]
    res = temp - df.shape[0]
    logger.info('delete {}'.format(res))
    return df

def link_geo(df, lon_col, lat_col, level_id = NEIGHS_ID):
    '''
    do a spacial join of the two dataframe
    '''
    logger.info("merging")
    geo_df = ut.convert_to_geodf(df, lon_col, lat_col)
    target_geo = ut.import_geometries(level_id)
    return ut.link_two_geos(geo_df, target_geo)

def split_crime(df, number = 10000):
   '''
   everytime give 10000 rows of data
   '''
   yield df.iloc[:number]
   logger.info('giving the subset of dataframe')
   df = df.iloc[number:]
   
if __name__ == '__main__':
    crime_df = lo.get_crime(2013,2013)
    count = 1
    for df in split_crime(crime_df):
        pdb.set_trace()
        logger.info("merging {} part of data".format(count))
        res = link_geo(df, 'longitude','latitude')
        res.to_csv('.\data\merged_after_{}.csv'.format(count))
    
