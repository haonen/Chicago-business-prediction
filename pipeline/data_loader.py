'''
Load data from web
'''
from sodapy import Socrata
import pandas as pd
import numpy as np
import datetime as dt

COL_TYPES = {'block': str, 
             'case_number': str,
             'community_area': str,
             'primary_type': 'category',
             'date': str,
             'latitude': float,
             'longitude': float,
             'year': int,
             'ward': int}
MAX_ROWS = 6839451 # the total rows of the original data

CRIME_DATA_ID = "6zsd-86xi"

def get_crime():
    '''
    Get 2017 and 2018 crime data from chicago data portal

    Return:
        pandas dataframe with the columns and dtypes as COL_TYPES
    '''
    cols = [item for item in COL_TYPES.keys()]
    client = Socrata('data.cityofchicago.org',
                     app_token,
                     username=,
                     password=)
    conds = "year = 2017 or year = 2018"
    res = client.get(CRIME_DATA_ID, 
                     select=",".join(cols),
                     where= conds,
                     limit = MAX_ROWS)
    client.close()
    df = pd.DataFrame.from_records(res)
    df = df[df['ward'].notna()].astype(COL_TYPES)
    df['date'] = pd.to_datetime(df['date'])
    return df
