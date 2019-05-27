import pandas as pd
import numpy as np

def summarize_missing_values(df):
    '''
    This function is used to summarize the missing values
    in specific columns in a given dataframe
    Inputs:
        df: dataframe
    Returns: disctionary with summary statistics of missing values
    '''
    missing_in_column_dict = {}
    for column in list(df.columns):
        column_null = df[df[column].isnull()]
        missing_in_column_dict[column] = (column_null.shape[0], df.shape[0])
    
    return missing_in_column_dict


def get_miss_columns(full_df):
    '''
    This function is used to find the columns with missing values in the given
    data set
    Inputs:
        full_df: dataframe
    Returns: the list of columns with missing values
    '''
    used_miss_list = []
    missing_dict = summarize_missing_values(full_df)
    for col_name, mis_col in missing_dict.items():
        if mis_col[0] != 0:
            used_miss_list.append(col_name)

    return used_miss_list


class community_mean_imputer:
    '''
    The class is designed to implement imputation with regional mean in given time
    '''
    def __init__(self, imputer_name):
        self.name = imputer_name
        self.trained_imp = {}

    def train_regional_mean(self, df, loc_column, time_column):
        '''
        The function is used to trian the model of imputation
        Inputs:
            df: dataframe
            loc_column: column represents the geographical unit
            time_column: column represents time unit
        Returns: the imputed trained dataframe
        '''
        #self.trained_impdf = pd.DataFrame(columns=list(df.columns))

        used_col_list = list(df.columns)
        for i in [loc_column, time_column]:
            used_col_list.remove(i)

        for col in used_col_list:
            print(col)

            for loc in list(df[loc_column].unique()):
                for year in list(df[time_column].unique()):
                    condition = (df[loc_column] == loc) & (df[time_column] == year)
                    df.loc[(condition & df[col].isnull()), col] = df.loc[condition, col].mean()

                    if (loc, year) not in self.trained_imp:
                        self.trained_imp[(loc, year)] = {}
                    self.trained_imp[(loc, year)][col] = df.loc[condition, col].mean()
 
        return df

    def transform_test(self, test_df, loc_column, time_column):
        '''
        This model is used to test the imputation model trained by the regional mean imputer
        Inputs:
            test_df: the testing dataframe
            loc_column: column represents the geographical unit
            time_column: column represents time unit
        Returns: imputed test dataframe
        '''
        used_col_list = list(df.columns)
        for i in [loc_column, time_column]:
            used_col_list.remove(i)

        for column in used_col_list:
            for loc_year, col_dict in self.trained_imp.items():
                loc, year = loc_year
                condition = ((test_df[column].isnull()) & (test_df[loc_column] == loc) & (test_df[time_column] == year))
                test_df.loc[condition, column] = col_dict[column]

        return test_df
        
