#!/usr/bin/python3
# -*-coding:utf-8 -*-
from AlgContract.algcontract.recall_contract import RecallAlgorithmContractExample
from AlgContract.algcontract.rank_contract import RankAlgorithmContractExample
from AlgContract.algcontract.recall_contract import write_success
import schedule
import time
import sys
import datetime
import os
from db import LollipopDB
import config


def write_strlist_to_file(str_list, file_path):
    if len(str_list) < 100:
        return -1
    with open(file_path, "w") as fw:
        for s in str_list:
            fw.write(s + "\n")
    return 0


def train_model():
    cur_ver = datetime.datetime.now().strftime("%Y%m%d")
    # cur_ver = "20220809"
    loldb = LollipopDB()
    recall_contract = RecallAlgorithmContractExample(True, cur_ver)
    # 从db中导出训练数据
    behavior_log_file = recall_contract.sample_dir_path
    start_t1 = (datetime.datetime.now() -
                datetime.timedelta(days=config.model_train_log_days)).strftime("%Y-%m-%d %H:%M:%S")
    behavior_data = loldb.get_user_features_behavior_log(start_t1)
    ret = write_strlist_to_file(behavior_data, behavior_log_file)
    if ret == -1:
        return

    forward_file = recall_contract.forward_local_dir
    start_t2 = (datetime.datetime.now() -
                datetime.timedelta(days=config.item_index_days)).strftime("%Y-%m-%d %H:%M:%S")
    forward_data = loldb.get_all_item_forward(start_t2)
    ret = write_strlist_to_file(forward_data, forward_file)
    if ret == -1:
        return
    write_success(os.path.dirname(behavior_log_file))

    recall_contract.train()
    recall_contract.build_index()
    rank_contract = RankAlgorithmContractExample(True, cur_ver)
    rank_contract.train()


def main():
    schedule.every().day.at("00:05").do(train_model)         # 每天在 00:05 时间点运行
    while True:
        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            # ----  立即执行（供测试用） ----
            schedule.run_all()  # 立即执行（供测试用）
            break
            # ----  立即执行（供测试用） ----
        else:
            print("waiting for daily training...")
            schedule.run_pending()   # 运行所有可以运行的任务
            time.sleep(1)


if __name__ == "__main__":
    main()
