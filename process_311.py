'''
Process and merge 311 dataset
Xuan Bu
'''

import pandas as pd
import data_loader as dl


DATA_IDS = {'Alley Lights Out': 't28b-ys7j', 'Tree Debris': 'mab8-y9h3',\
         'Abandoned Vehicles': '3c9v-pnva',\
         'Garbage Carts': '9ksk-na4q', 'Graffiti Removal': 'hec5-y4x5',\
         'Rodent Baiting': '97t6-zrhs', 'Tree Trims': 'uxic-zsuj',\
         'Sanitation Code Complaints': 'me59-5fac',\
         'Street Lights - All Out': 'zuxi-7xem',\
         'Street Lights - One Out': '3aav-uy2v'}


def process_311(data_ids):
    '''
    Process and merge 311 data set.
    Inputs:
        data_ids: (dictionary) of different complaint and its id
    Returns:
        a merged dataframe of the amount of different type of 311
    '''
    merged_df = pd.DataFrame(columns=['zip_code','year'])
    for c, d_id in data_ids.items():
        df = dl.get_311(d_id)
        df['year'] = df['creation_date'].str[:4]
        n_df = df.groupby(['zip_code', 'year']).size()\
                 .reset_index().rename(columns={0: c})
        merged_df = pd.merge(merged_df, n_df, how='outer',\
                             left_on=['zip_code','year'],\
                             right_on =['zip_code','year'])
    merged_df = merged_df.astype({'year': int, 'zip_code': int})
    processed_df = merged_df[(merged_df['year'] >= 2012)\
                            & (merged_df['year'] <= 2017)]
    processed_df = processed_df.fillna(0)
    
    return processed_df


df = processed_df(DATA_IDS)
vab = dl.get_311("7nii-7srd")
new_vab = vab.groupby(['zip_code']).size().reset_index()
             .rename(columns={0: 'Vacant and Abandoned Buildings Reported'})
new_vab = new_vab.astype({"zip_code": int})
new_df = pd.merge(df, new_vab,  how='outer',\
                            left_on=['zip_code'], right_on = ['zip_code'])
new_df.to_csv('311.csv', sep=',')


