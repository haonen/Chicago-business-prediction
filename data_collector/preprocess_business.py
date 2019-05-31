"""
Project: preprocess_business
Yuwei Zhang
"""

import pandas as pd
import numpy as np


def read_data(path, indexcol,datecol):
    df = pd.read_csv(path, index_col=indexcol, parse_dates=datecol)
    return df


def compute_period(date_issued, change_date, expiration_date):
    if pd.isnull(change_date):
        early_date = expiration_date
    elif pd.isnull(expiration_date):
        early_date = change_date
    else:
        early_date = min(change_date, expiration_date)
    return early_date - date_issued


def check_death(df, date_issued, change_date, expiration_date, outcome_col, year_period):
    df['death_period'] = df.apply(lambda x: compute_period(x[date_issued], x[change_date], x[expiration_date]), axis=1)
    df[outcome_col] = np.where(df['death_period'] < year_period, 1, 0)



def create_indicator(df, issue_date, change_date, expiration_date, year):
    df['start_year'] = pd.to_numeric(df[issue_date].dt.year)
    df['end_year'] = df.apply(lambda x: x[expiration_date] if x[expiration_date] <= x[change_date] or pd.isnull(x[change_date]) else x[change_date], axis=1)
    df['end_year'] = pd.to_numeric(df['end_year'].dt.year)
    df[str(year) + "ind"] = 0
    df.loc[((year >= df['start_year']) & (year <= df['end_year'])), str(year) + "ind"] = 1
    sub_df = df[df[str(year) + "ind"] == 1]
    sub_df['year'] = year
    sub_df = sub_df.drop(columns=[str(year) + "ind"])
    df = df.drop(columns=[str(year) + "ind"])
    return df, sub_df

#This loop is used for pivoting all the crime data into wide type and concat them
for year in range(2012, 2018):
    file_path = 'D:/UChicago/2019 spring/CAPP30254/assignments/Project/crime data/{}_res.csv'.format(year)
    df = pd.read_csv(file_path, dtype={'zip': 'str', 'year': 'str'})
    df = df.pivot(index='zip', columns='primary_type', values='count')
    df = df.reset_index()
    df['year'] = str(year)
    df['zip'] = df.apply(lambda x: re.match(r"(\d{5})(.0)", x['zip']).group(1), axis=1)
    crime_data = pd.concat([crime_data, df])

#The following code are used for mergeing 311, acs and crime into business license
merge_data = pd.merge(concat_license, acs, how='left', on=['year', 'zip_code'])
merge_data = pd.merge(merge_data, data311, how='left', on=['year', 'zip_code'])
merge_data = pd.merge(merge_data, crime_data, how='left', on=['year', 'zip_code'])

#These code is used for imputate the vacancy in same_house varible of acs 2013
sub_2012 = df[df["year"] == 2012][["zip_code", "same_house"]]
sub_2013 = df[df["year"] == 2013]
full = pd.merge(sub_2012, sub_2013, left_on="zip_code", right_on="zip_code")
full = full[full.columns.remove("same_house_x")]

df = df[df["year"] != 2013]
df = pd.concat([full, df], join="inner")


def create_outcome(df, outcome, date_issued, change_date, expiration_date):
    '''
    Define the whether a license dies in a year and define its duration
    :param df: a data frame
    :param outcome: 1 is dead and 0 is alive
    :param date_issued: the colname of license issue date
    :param change_date: the colname of license status change date
    :param expiration_date: the colname of license term expiration date

    :return: a modified data frame
    '''
    df['cut_off_date'] = df.apply(lambda x: pd.Timestamp(x['year'] + 1, 12, 31), axis=1)
    df['end_date'] = df.apply(lambda x: x[expiration_date] if x[expiration_date] <= x[change_date] or pd.isnull(x[change_date]) else x[change_date], axis=1)
    df[outcome] = np.where(df['end_date'] < df['cut_off_date'], 1, 0)
    df['early_date'] = df.apply(lambda x: min(x['end_date'], x['cut_off_date']), axis=1)
    df['duration'] = df['early_date'] - df[date_issued]
    return df.drop(columns=['early_date', 'end_date', 'cut_off_date'])
