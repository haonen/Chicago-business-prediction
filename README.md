# Chicago-business-prediction

Implement a machine learning pipeline to predict whether the business in Chicago will survive their first 2 years 

## Getting Started

Get the full dataset
 
```
cd data
sh get_fullfiles.sh
```

### Prerequisites


All the packages' requirement is in the enviorment.yml

To clone the enviorment, simply run the following:

```
conda env create -f environment.yml
```

To activate the enviorment, simply run the following:

```
conda activate myenv
```

### Installing

```
python setup.py install
```

## Running the tests

```
py.test
```

## Running the pipeline

```
python main.py --config ./cofigs/acs_geo.yml
```
In the configs file, there are different combination of features that from ACS, reported 311, reported Crime, business license that you can choose.


## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Satej 
* Inspiration
* etc