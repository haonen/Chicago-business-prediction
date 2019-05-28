* step 1: read in the final_data.csv as a data frame
* step 2: split the df into X(X = df.drop(columns=['license death']) and y (y = df[['license death']].values)
* step 3: min_year = 2012, max_year = 2018, loc_column='ward', time_column='year', categorical_col= ['application type','conditional approval','duration','license description', 'ward', 'zip code']
         k = 30
* step 4: model_list: (list of str) a list of names of models; clfs: (dict) a dictionary of base classifiers; grid:(dict) parameters grid, 
         threshold = ; save_path: the path to save all plots
* step 5: implement the wrap_up() in Ipython or notebook and pass all the parameters
