'''
Generate Feature
'''

import pandas as pd
import preprocess_business as pb


COLS_TO_DIVIDE_POP = ['health coverage population', 'same house',\
'alley lights out', 'abandoned vehicles', 'garbage carts',\
'graffiti removal', 'rodent baiting', 'sanitation code complaints',\
'street lights - all out', 'street lights - one out', 'tree debris',\
'tree trims', 'poverty rate', 'arson', 'assault', 'battery',\
'burglary', 'crim sexual assault', 'homicide',\
'motor vehicle theft', 'robbery', 'theft']

COLS_TO_RESERVE = ['application type', 'conditional approval', \
       'license description', 'ward', 'zip code',\
       'total population', 'median household income', 'gini index',\
       'health coverage population', 'poverty rate', 'unemployment rate',\
       'alley lights out', 'alley lights out completion rate',\
       'abandoned vehicles', 'abandoned vehicles completion rate',\
       'garbage carts', 'garbage carts completion rate', 'graffiti removal',\
       'graffiti removal completion rate', 'rodent baiting',\
       'rodent baiting completion rate', 'sanitation code complaints',\
       'sanitation code complaints completion rate', 'street lights - all out',\
       'street lights - all out completion rate', 'street lights - one out',\
       'street lights - one out completion rate', 'tree debris',\
       'tree debris completion rate', 'tree trims',\
       'tree trims completion rate', 'duration', 'arson', 'assault', 'battery',\
       'burglary', 'crim sexual assault', 'homicide', 'motor vehicle theft',\
       'robbery', 'theft', 'in zip', 'same house', 'license death',\
       'health coverage population per capita', 'same house per capita',\
       'alley lights out per capita', 'abandoned vehicles per capita',\
       'garbage carts per capita', 'graffiti removal per capita',\
       'rodent baiting per capita', 'sanitation code complaints per capita',\
       'street lights - all out per capita',\
       'street lights - one out per capita', 'tree debris per capita',\
       'tree trims per capita', 'poverty rate per capita', 'arson per capita',\
       'assault per capita', 'battery per capita', 'burglary per capita',\
       'crim sexual assault per capita', 'homicide per capita',\
       'motor vehicle theft per capita', 'robbery per capita',\
       'theft per capita']

INDEXCOL = 'ID'
DATECOL = ['APPLICATION CREATED DATE', 'LICENSE TERM START DATE',\
           'LICENSE TERM EXPIRATION DATE', 'DATE ISSUED',\
           'LICENSE STATUS CHANGE DATE']


def rename_cols(df):
    '''
    Rename the columns of the dataframe.
    Inputs:
        df: dataframe
    Returns:
        dataframe with renamed columns
    '''
    cols = list(df.columns)
    for col in cols:
        ncol = col.lower()
        ncol = ncol.replace('_', ' ')
        df = df.rename(columns={col: ncol})
    return df


def calculate_col_per_capita(cols):
    '''
    Given the certain columns, then calculate the number of
    every column per capita.
    Inputs:
        cols: (list) of names of columns
    '''
    for col in cols:
        new_col = col + ' per capita'
        if col == 'same house':
            df[new_col] = 1 - df[col] / df['total population']
        else:
            df[new_col] = df[col] / df['total population']
    return None


df = pb.read_data('../Downloads/updated_data.csv', INDEXCOL, DATECOL)
df = pb.create_outcome(
    df, 'license death', 'DATE ISSUED', 'LICENSE STATUS CHANGE DATE', 'LICENSE TERM EXPIRATION DATE')
df = rename_cols(df)
calculate_col_per_capita(COLS_TO_DIVIDE_POP)
final_df = df[COLS_TO_RESERVE]
final_df.to_csv('final_data.csv')




