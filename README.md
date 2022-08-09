# usage
### set up mysql DB
please use run_mysql.sh and db_schema.sql to init a DB instance, remember to modify db connect string in config.py.
### init train cu model
```shell
cd AlgContract/algcontract/ & python cu_contract.py
```
### init train recall&rank model
```shell
python model_trainer.py test
```
### start daily train recall&rank model job
```shell
python model_trainer.py
```
### start content_miner service
```shell
python content_miner.py
```
### test content_miner service
```shell
python content_miner_test.py
```
### start recommender service
```shell
python recommender.py
```
### test recommender service
```shell
python recommend_test.py
```

