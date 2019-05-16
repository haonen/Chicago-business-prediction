"""
Project: preprocess_business
Yuwei Zhang
"""

import pandas as pd
import numpy as np


def read_data(path, indexcol, data_type, datecol):
    df = pd.read_csv(path, index_col=indexcol, dtype=data_type, parse_dates=datecol)
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





