import pandas as pd
import numpy as np

table_dict = {"total_population": {"table": "B01003", "zip": "GEO.id2", "variable":"HD01_VD01"}, 
              "median_household_income": {"table": "B19013", "zip": "GEO.id2", "variable":"HD01_VD01"},
              "gini_index": {"table": "B19083", "zip": "GEO.id2", "variable":"HD01_VD01"},
              "health_coverage_population": {"table": "B992701", "zip": "GEO.id2", "variable":"HD01_VD02"},
              "same_house": {"table": "B07012", "zip": "GEO.id2", "variable":"HD01_VD06"},
              "poverty_rate": {"table": "S1701", "zip": "GEO.id2", "variable":"HC02_EST_VC01"}}
unemp_dict = {"unemployment_rate": {"table": "S2301", "zip": "GEO.id2", "variable":"HC04_EST_VC01"},
              "unemployment_rate2": {"table": "DP03", "zip": "GEO.id2", "variable":"HC03_VC07"}}

def read_ACS(year_list, table_dict, unemp_dict):
    '''
    The function is used to read the ACS files
    Inputs:
        year_list: list of year to read
        table_dict: dictionary of tables to read
        unemp_dict: dictionary used to distingunish table of unemployment usage in different years
    Return: df dictionary of different tables in different years
    '''
    data_dict = {}
    for year in year_list:
        for t_name, value in table_dict.items():
            if (year == 13) and (t_name == "same_house"):
                pass

            else:
                table_name = t_name + str(year)
                df = pd.read_csv(r"ACS_" + str(year) + "_" + \
                                 value["table"] + "_" + t_name + ".csv")
                data_dict[table_name] = [df.iloc[1:], value]

        if (year == 12) or (year == 13) or (year == 14):
            emp_table_name = "unemployment_rate" + str(year)
            df = pd.read_csv(r"ACS_" + str(year) + "_" + \
                                 unemp_dict["unemployment_rate"]["table"] + "_" + "unemployment_rate" + ".csv")
            data_dict[emp_table_name] = [df.iloc[1:], unemp_dict["unemployment_rate"]]

        else:
            emp_table_name = "unemployment_rate" + str(year)
            df = pd.read_csv(r"ACS_" + str(year) + "_" + \
                                 unemp_dict["unemployment_rate2"]["table"] + "_" + "unemployment_rate" + ".csv")
            data_dict[emp_table_name] = [df.iloc[1:], unemp_dict["unemployment_rate2"]]

    return data_dict


def ACS_select(df_dict):
    '''
    The function is used to select and rename target features from ACS dataframe
    Inputs:
        df_dict: df dictionary of different tables in different years
    Returns: data dictionary in year
    '''
    new_df_dict = {}
    yearly_data = {}
    for df_name, df_value in df_dict.items():
        variable, year = df_name[:-2], df_name[-2:]
        
        df_v = df_value[1]
        df = df_value[0][[df_v["zip"], df_v["variable"]]]
        new_df_dict[df_name] = {df_v["zip"]:"zipcode", df_v["variable"]:variable}
        df = df.rename(columns=new_df_dict[df_name])

        if year not in yearly_data:
            yearly_data[year] = df
        else:
            yearly_data[year] = pd.merge(df, yearly_data[year], left_on="zipcode", right_on="zipcode")
    
    same_home13 = pd.DataFrame({"zipcode": yearly_data["13"]["zipcode"],"same_house":([np.nan] * yearly_data["13"].shape[0])})
    yearly_data["13"] = pd.merge(yearly_data["13"], same_home13, left_on="zipcode", right_on="zipcode")
        
    return yearly_data


def ACS_integrater(yearly_data):
    '''
    The function is used to integrate ACS data from different years
    Input:
        yearly_data: data dictionary in year
    Return: full ACS df
    '''
    ordered_column = ["zipcode", "total_population", "median_household_income", "gini_index", 
                                     "health_coverage_population", "same_house", "poverty_rate",
                                     "unemployment_rate", "year"]
    full_df = pd.DataFrame(columns=ordered_column)

    for year, df in yearly_data.items():
        df["year"] = year
        df = df[ordered_column]
        full_df = pd.concat([full_df, df], join="inner")
    
    return full_df


def ACS_do(year_list, table_dict, unemp_dict):
    '''
    '''
    data_dict = read_ACS(year_list, table_dict, unemp_dict)
    yearly_data = ACS_select(data_dict)
    full_df = ACS_integrater(yearly_data)
    return full_df


full_df = ACS_do([12,13,14,15,16,17], table_dict, unemp_dict)
full_df.to_csv("ACS_full.csv")