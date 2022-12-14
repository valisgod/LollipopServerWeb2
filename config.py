#!/usr/bin/python3
# -*-coding:utf-8 -*-
import os

# db地址
lollipop_db_conn = os.environ['JAWSDB_URL']
# 计算用户特征使用流水时长(天)
user_features_calc_log_days = 7
# 训练recall/rank模型使用流水时长(天)
model_train_log_days = 7
# 构建item索引使用数据时长(天)
item_index_days = 30
