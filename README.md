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
source activate doc_env
source deactivate
```
(or replace 'source' by '.')

* Install requirements

```
while read requirement; do python -m pip install -U $requirement; done < requirements.txt
```