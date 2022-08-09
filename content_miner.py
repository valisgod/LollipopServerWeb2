#!/usr/bin/python3
# -*-coding:utf-8 -*-
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import json
from AlgContract.algcontract.cu_contract import ContentUnderstandingAlgorithmContractExample
from db import LollipopDB


contract = ContentUnderstandingAlgorithmContractExample()
print("cu model path: {}".format(contract.model_ar_dir))
loldb = LollipopDB()


@dispatcher.add_method(name="AddContent")
def ask_recommend(**kwargs):
    raw_content = kwargs["raw_content"]
    # id统一用string类型
    item_id = str(raw_content['id'])
    # 存储原始item内容
    loldb.write_item_raw_content(item_id, json.dumps(raw_content))
    # 执行内容理解合约
    forward_info = contract.parse([raw_content])[0]
    # 存储item正排信息
    loldb.write_item_forward(item_id, json.dumps(forward_info))
    return "OK"


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4001, application)
