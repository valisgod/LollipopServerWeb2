#!/usr/bin/python3
# -*-coding:utf-8 -*-
import requests
import json


def main():
    url = "http://localhost:4001/jsonrpc"

    with open("./AlgContract/data/test/items.json", "r", encoding="utf-8") as f:
        for line in f:
            document = json.loads(line.strip())
            payload = {
                "method": "AddContent",
                "params": {
                    "raw_content": document,
                },
                "jsonrpc": "2.0",
                "id": 0,
            }
            response = requests.post(url, json=payload).json()
            print(response)

            assert response["jsonrpc"]
            assert response["id"] == 0
            break


if __name__ == "__main__":
    main()