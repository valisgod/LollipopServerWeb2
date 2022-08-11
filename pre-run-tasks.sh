#!/bin/bash

### init train cu model
cd AlgContract/algcontract/ && python cu_contract.py

### init train recall&rank model
python model_trainer.py test
