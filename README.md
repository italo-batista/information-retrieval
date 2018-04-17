
This repository will contain some reports about fundamentals of information retrieval. Problems and concepts here explored are guided by Information Retrieval classes from Computer Science course at UFCG 2018.1 (professor: Leandro Balby). 

Main bibliography references are:

 - Introduction to Information Retrieval. Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze. Cambridge 2009.
 - Information Retrieval: Implementing and Evaluating Search Engines. Stean Bütcher, Charles L.A. Clarke, Gordon V. Cormack. MIT 2010


## Set up env

* [Download](https://www.anaconda.com/download/#linux) and install Anaconda

```
curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
```

* Install it

```
bash Anaconda3-5.\*\.sh
```

* Press ENTER while installing to read license

* Enter yes to install

* Specify instalation location (~/../../home/anaconda3)

* Update conda

```
conda update -n base conda
```

* Create enviroment

```
conda create --name rec-info-env python=3
```

* Usage

```
source activate rec-info-env
source deactivate
```
(or replace 'source' by '.')

* Install requirements

```
while read requirement; do python -m pip install -U $requirement; done < requirements.txt
```