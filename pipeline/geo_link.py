'''

Link the crime data with the neighborhood geom dataframe

'''

import data_loader as lo
import pandas as pd
import neighborhoods as nb
import logging
import sys

logger = logging.getLogger('merging')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('./debug.log')
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
    geo_df = nb.convert_to_geodf(df, lon_col, lat_col)
    target_geo = nb.import_geometries(level_id)
    return nb.link_two_geos(geo_df, target_geo)





