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


## Getting results

The results of the pipeline is saved in the output folder. 

Under the performance foler, there would be csvs to keep all the performance of all models

Under the pr folder, there would be precison-recall graphs

Under the roc foler, there would be roc graphs

## Authors

* **Peng Wei**  [CV](https://pengwei715.github.io/)
* **Yuwei Zhang**  [Linkedin](https://www.linkedin.com/in/yuwei-zhang-b3b597102/)
* **Ta-yun Yang**  [Linkedin](https://www.linkedin.com/in/ta-yun-yang-9a3539171/)
* **Xuan Bu**  [Linkedin](https://www.linkedin.com/in/xuanbu/)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This project is the final project of machine learning for public policy in University of Chicago.  

* Supervised by Professor [Rayid Ghani](https://github.com/dssg/MLforPublicPolicy) 
* Inspired by [Satej](https://github.com/satejsoman) 