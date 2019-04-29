#!/usr/bin/env python3
'''
Load data from web
'''
from sodapy import Socrata
import pandas as pd
import numpy as np
import datetime as dt
from census import Census
from us import states
import pdb

def get_311(start_year, end_year):
    '''
    Get 2012 and 2017 311 data from chicago data portal

    Input:
        start_year: timestamp '"2017-12-31T20:00:05.000"'format
        end_time: timestamp  '"2017-12-31T20:00:05.000"' format

    Return:
        pandas dataframe with the columns and dtypes as COL_TYPES
    '''   
    COL_TYPES = {'st_type': str, 
                 'created_date': str,
                 'zip_code': float,
                 'longitude': float,
                 'lattitude': int} 
    DATA_ID = "v6vf-nfxy"
    cols = [item for item in COL_TYPES.keys()]
    client = Socrata('data.cityofchicago.org', 
                     'Lfkp6VmeW3p5ePTv0GhNSmrWh',
                     username="pengwei@uchciago.edu",
                     password="2h1m@k@1men")

    conds = "created_date between {} and {}"\
            .format(start_year, end_year)  
    res = client.get(DATA_ID, 
                     select=",".join(cols),
                     where= conds)
    client.close()
    df = pd.DataFrame.from_records(res)
    df = df.astype(COL_TYPES)
    df['year'] = pd.to_datetime(df['created_date'])
    return df

def get_acs_data(start_year, end_year):
    '''
    Get the information from census data
    Total population, white population, black population,
    high school degree population, household income

    Return:
        pandas dataframe
    '''
    NAMES_DIC = {'B01001_001E': "population", 
             'B19013_001E': "median_household_income", 
             'B19083_001E': "gini_index", 
             'B992701_002E': "health_coverage_population",
             'B07012_005E': 'same_house_one_year_ago',
             'B10059_002E': 'income_in_the past_12_months_below_poverty_rate'}  
    c = Census('3eb1575454b4de2cf12e0072bd946ecb852579d2')
    lst_df = []

    for item in range(start_year, end_year+1):
        res = c.acs5.get(('NAME', 
                   'B01001_001E',
                   'B19013_001E',
                   'B19083_001E',
                   'B992701_002E',
                   'B07012_005E',
                   'B10059_002E'
                   ),
                   {'for': 'block group',
                   'in': 'state: {} county: {}'.format('17','031')},
                   year = item)
        df = pd.DataFrame.from_records(res)
        df.rename(columns=NAMES_DIC,inplace=True)
        df.drop(columns =['NAME'], axis=1, inplace=True)
        df['geoid'] = df["state"] + df["county"] + df["tract"]
        df['year'] = item
        lst_df.append(df)
    pdb.set_trace()
    return pd.concat(lst_df)

def get_crime(start_year, end_year):
    '''
    Get 2013 to 2018 crime data from chicago data portal

    Return:
        pandas dataframe with the columns and dtypes as COL_TYPES
    '''
    crime_type = ["HOMICIDE",
                  "CRIM SEXUAL ASSAULT",
                  "ROBBERY","ASSAULT",
                  "BATTERY",
                  "BURGLARY",
                  "ARSON", 
                  "MOTOR VEHICLE THEFT",
                  "THEFT"]
    COL_TYPES = {'block': str, 
                 'case_number': str,
                 'primary_type': 'category',
                 'date': str,
                 'latitude': float,
                 'longitude': float,
                 'year': int}
    MAX_ROWS = 6839451 # the total rows of the original data
    CRIME_DATA_ID = "6zsd-86xi"
    cols = [item for item in COL_TYPES.keys()]
    client = Socrata('data.cityofchicago.org',
                     'Lfkp6VmeW3p5ePTv0GhNSmrWh',
                     username='pengwei@uchciago.edu',
                     password='2h1m@k@1men')
    conds = "year >= {} AND year <= {}".format(start_year, end_year)
    res = client.get(CRIME_DATA_ID, 
                     select=",".join(cols),
                     where= conds,
                     limit = MAX_ROWS)
    client.close()
    df = pd.DataFrame.from_records(res)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.primary_type.isin(crime_type)]
    return df