#!/usr/bin/python3
# -*-coding:utf-8 -*-
import requests
import json


def main():
    url = "https://recommend-server-web2.herokuapp.com/jsonrpc"

    with open("./AlgContract/data/test/user_local_log.json", "r", encoding="utf-8") as f:
        for line in f:
            document = json.loads(line.strip())
            payload = {
                "method": "ReportUserBehavior",
                "params": {"uid": document["uid"],
                           "user_behavior_log": document
                           },
                "jsonrpc": "2.0",
                "id": 0,
            }
            response = requests.post(url, json=payload).json()
            print(response)
            break

    payload = {
        "method": "AskRecommend",
        "params": {"uid": "000",
                   "item_nums": 4
                   },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, json=payload).json()
    print(json.dumps(response, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
