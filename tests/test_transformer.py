'''
test code for the transformer
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import OrderedDict
import unittest
import transformer
import pandas as pd
import pdb

CONFIG = {
              'dummy':{
                'cols' : ["zip code","application type","conditional approval","license description", "duration"],
                'k': [30]
              },
              'imputation':{ 
                  'cols': ["zip code","application type","conditional approval","license description", "duration"], 
                'loc_col': ["ward"],
                'time_col': ["year"]},
                'scaling':
                {'cols': ['theft']}
           } 

TEST_FILE = '../data/test0.csv'
TRAIN_FILE = '../data/train0.csv'

class TestTransformer(unittest.TestCase):
    '''
    unit test for the Transformer
    '''
    def test_(self):
        
        x_train =  pd.read_csv(TRAIN_FILE)
        x_test = pd.read_csv(TEST_FILE)
        transformer.transform(CONFIG, x_train, x_test)
        
if __name__ == '__main__':
    unittest.main()
           
        
