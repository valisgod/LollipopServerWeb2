#!/bin/bash

### init train cu model
#cd AlgContract/algcontract/ && python cu_contract.py
#cd -

# run model trainer
nohup python model_trainer.py > ./model_trainer.log &

# start recommender
python recommender.py $1
