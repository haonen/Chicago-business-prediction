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
import argparse
import os
import sys

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

def split_crime(df, number = 1000):
   '''
   everytime give 10000 rows of data
   '''
   logger.info('giving the subset of dataframe')
   while df.shape[0]:
       yield df.iloc[:number]
       df = df.iloc[number:]

def process_crime(df, year, part_num):
    '''
    processing the crime data
    '''
    logger.info('begin to processing year {} part {}'.format(year, part_num))
    res = link_geo(df, 'longitude','latitude')
    #pdb.set_trace()
    res = res.drop(['longitude','latitude','coordinates','index__neig','objectid'], axis=1)
    filename = 'crime_{}_{}.csv'.format(year, part_num)
    res.to_csv(filename)

def run_crime(args):
    year = args.year
    num = args.number
    crime_df = lo.get_crime(year,year)
    temp = split_crime(crime_df,num)
    count = 1
    for df in temp:
        logger.info("merging year {} data".format(year))
        process_crime(df,year,count)
        count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pass year and number of data') 
    parser.add_argument('--year', dest='year', type=int, default=2013)
    parser.add_argument('--number', dest ='number', type=int, default =1000)
    args = parser.parse_args()
    run_crime(args) 
