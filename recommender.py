#!/usr/bin/python3
# -*-coding:utf-8 -*-
import datetime
import sys
import config
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import json
from jsonrpc import JSONRPCResponseManager, dispatcher
from AlgContract.algcontract.recall_contract import RecallAlgorithmContractExample
from AlgContract.algcontract.rank_contract import RankAlgorithmContractExample
from AlgContract.algcontract.user_contract import UserContractExample
from AlgContract.algcontract.cu_contract import ContentUnderstandingAlgorithmContractExample
from db import LollipopDB


# 启动时加载训练完成的最新版本模型
cu_contract = ContentUnderstandingAlgorithmContractExample()
print("cu model path: {}".format(cu_contract.model_ar_dir))
loldb = LollipopDB()
recall_contract = RecallAlgorithmContractExample()
print("recall model path: {}".format(recall_contract.last_model_local_dir))
print("recall index path: {}".format(recall_contract.index_local_dir))
rank_contract = RankAlgorithmContractExample()
print("rank model path: {}".format(rank_contract.model_local_dir))
user_contract = UserContractExample()
loldb = LollipopDB()


@dispatcher.add_method(name="AskRecommend")
def ask_recommend(**kwargs):
    # id统一用string类型
    uid = str(kwargs["uid"])
    item_nums = kwargs["item_nums"]
    # 通过uid从db中获取计算好的user_features
    user_features = json.loads(loldb.get_user_fearures(uid))
    # 查询已经推荐过的item列表
    his_rec_items = loldb.get_user_rec_items(uid)
    # 执行召回合约, 过滤his_rec_items
    recall_items = recall_contract.recall(user_features, item_nums * 10, his_rec_items)
    # 执行排序合约
    recomm_result = rank_contract.rank(recall_items, user_features, item_nums)
    # 存储推荐结果
    loldb.write_recommmend_log(uid, recomm_result)
    return recomm_result


@dispatcher.add_method(name="ReportUserBehavior")
def report_user_behavior(**kwargs):
    # id统一用string类型
    uid = str(kwargs["uid"])
    user_behavior_log = kwargs["user_behavior_log"]
    # store behavior log in db
    loldb.write_user_behavior_log(uid, json.dumps(user_behavior_log))
    # 汇总此用户最近一段时间内db中历史流水
    start_time = (datetime.datetime.now() -
                  datetime.timedelta(days=config.user_features_calc_log_days)).strftime("%Y-%m-%d %H:%M:%S")
    merged_log = loldb.get_merged_user_behavior_log(uid, start_time)
    # 执行用户特征计算合约
    user_fearures = user_contract.update_user_interest(merged_log)
    # 记录用户特征到db
    loldb.write_user_features(uid, json.dumps(user_fearures, ensure_ascii=False))
    return "OK"


@dispatcher.add_method(name="AddContent")
def ask_recommend(**kwargs):
    raw_content = kwargs["raw_content"]
    # id统一用string类型
    item_id = str(raw_content['id'])
    # 存储原始item内容
    loldb.write_item_raw_content(item_id, json.dumps(raw_content, ensure_ascii=False))
    # 执行内容理解合约
    forward_info = cu_contract.parse([raw_content])
    if len(forward_info) == 0:
        raise Exception("content understanding failed.")
    # 存储item正排信息
    loldb.write_item_forward(item_id, json.dumps(forward_info[0], ensure_ascii=False))
    return "OK"


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    # TODO new feature: 启动一个异步任务, 后台持续增量构建item索引 & 增量写入正排, 提升item召回时效性
    run_simple('0.0.0.0', int(sys.argv[1]), application)
