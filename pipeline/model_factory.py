'''
Model class for the pipeline
credit to satejsoman
'''
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from yaml
import heapq

class model_factory():
    '''
    model factory generate the next aviable model
    ''' 
    def __init__(self, file = None):
        default_models =  Queue()
        if not file:
           for models in default_models:
               for model in models:
                   yield model
        else:
            with open('config.yaml') as config_file:
                config = yaml.safe_load(config_file)
                for (model, params) in config_dict.items():
                    constructor = globals()[model]
                    model_parameters += [{generate_name(model, params.keys(), vals): constructor(**dict(zip(params.keys(), vals)))} for vals in product(*params.values())]
        return Grid(model_parameters)
