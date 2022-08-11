# Run Process Mannally
### set up mysql DB
please use run_mysql.sh and db_schema.sql to init a DB instance, remember to modify db connect string in config.py.
### init train cu model
```shell
cd AlgContract/algcontract/ && python cu_contract.py
```
### init train recall&rank model
```shell
python model_trainer.py test
```
### start daily train recall&rank model job
```shell
python model_trainer.py
```
### start recommender&content_miner service
```shell
python recommender.py $port
```
### test recommender service
```shell
python recommend_test.py
```
### test content_miner service
```shell
python content_miner_test.py
```

# Deploy On Heroku
Since this git repo contains submodule which is not well supported by Heroku, deployment can only be done by git push (cannot by web UI):
```
git push https://git.heroku.com/recommend-server-web2.git master
```
and then scale web dynos to at least 1:
```
heroku ps:scale web=1 -a recommend-server-web2
```