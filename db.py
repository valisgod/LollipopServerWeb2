#!/usr/bin/python3
# -*-coding:utf-8 -*-
import sqlalchemy as sa
import config
import pickle
import json
from sqlalchemy.orm import sessionmaker
import warnings
import pandas as pd
import random

warnings.filterwarnings('ignore')


def commastr(lst, sep=','):
    return sep.join(map(str, lst))


def read_sql(self, ssql, nidxcol=0, **kwargs):
    df = pd.read_sql(ssql, self, **kwargs)
    return df.set_index(list(df.columns)[:nidxcol]) if nidxcol else df


def dump_df(df, filename):
    pickle.dump(df, open(filename, 'wb'))
    return


class MDB():
    def __init__(self, conn_str, *args, **kwargs):
        self.db = sa.create_engine(conn_str, server_side_cursors=True)
        sa.engine.Engine.read_sql = read_sql
        self.Session = sessionmaker(bind=self.db)


class LollipopDB(MDB):
    def __init__(self, *args, **kwargs):
        self.conn_str = config.lollipop_db_conn
        super().__init__(self.conn_str, *args, **kwargs)

    def write_item_raw_content(self, item_id, raw_content):
        session = self.Session()
        command = "REPLACE INTO t_item_raw_content(item_id,raw_content,created_at) " \
                  "VALUES (:item_id,:raw_content,now()) "
        session.execute(command, {"item_id": item_id,
                                  "raw_content": raw_content})
        session.commit()
        session.close()
        return

    def write_item_forward(self, item_id, forward_info):
        session = self.Session()
        command = "INSERT INTO t_item_forward(item_id,forward_info,updated_at,created_at) " \
                  "VALUES (:item_id,:forward_info,now(),now()) " \
                  "on DUPLICATE KEY UPDATE forward_info=:forward_info,updated_at=now()"
        session.execute(command, {"item_id": item_id,
                                  "forward_info": forward_info})
        session.commit()
        session.close()
        return

    def get_item_forward(self, item_id):
        command = "SELECT forward_info from t_item_forward where item_id='{}'".format(
            item_id)
        forward_info = json.loads(self.db.read_sql(command)[
                                  'forward_info'].values[0])
        return forward_info

    def get_all_item_forward(self, start_time):
        command = "SELECT item_id,forward_info from t_item_forward where updated_at>'{}'".format(
            start_time)
        forward_info = self.db.read_sql(command)['forward_info'].values
        return forward_info

    def write_user_behavior_log(self, uid, behavior_log):
        session = self.Session()
        command = "REPLACE INTO t_user_behavior_log(uid,user_behavior_log,created_at) " \
                  "VALUES (:uid,:user_behavior_log,now()) "
        session.execute(command, {"uid": uid,
                                  "user_behavior_log": behavior_log})
        session.commit()
        session.close()
        return

    def get_user_features_behavior_log(self, start_time):
        command = "SELECT user_behavior_log,user_features from t_user_behavior_log t1, t_user_features t2 " \
            "where t1.uid = t2.uid and t1.created_at>'{}'".format(start_time)
        db_res = self.db.read_sql(command)
        train_data = []
        for log, features in zip(db_res["user_behavior_log"], db_res["user_features"]):
            train_data.append(
                json.dumps({"docs": json.loads(log)['docs'], "user_feature": json.loads(features)}))
        return train_data

    def get_merged_user_behavior_log(self, uid, start_time):
        command = "SELECT user_behavior_log from t_user_behavior_log where uid='{}' " \
                  "and created_at > '{}'".format(uid, start_time)
        behavior_logs = self.db.read_sql(command)['user_behavior_log'].values
        merged_logs = []
        for logs in behavior_logs:
            merged_logs += json.loads(logs)["docs"]
        return merged_logs

    def write_user_features(self, uid, user_features):
        session = self.Session()
        command = "INSERT INTO t_user_features(uid,user_features,updated_at,created_at) " \
                  "VALUES (:uid,:user_features,now(),now()) " \
                  "on DUPLICATE KEY UPDATE user_features=:user_features,updated_at=now()"
        session.execute(command, {"uid": uid,
                                  "user_features": user_features})
        session.commit()
        session.close()
        return

    def get_user_fearures(self, uid):
        command = "SELECT user_features from t_user_features where uid='{}'".format(
            uid)
        user_features = self.db.read_sql(command)['user_features'].values
        if len(user_features) != 0:
            return user_features[0]
        command1 = 'SELECT user_features from t_user_features limit 10'
        user_features_10 = self.db.read_sql(command1)['user_features'].values
        if len(user_features_10) == 0:
            raise Exception('No existing user in db')
        return random.choice(user_features_10)

    def write_recommmend_log(self, uid, recomm_result):
        session = self.Session()
        recomm_id_list = []
        for item in recomm_result:
            recomm_id_list.append(str(item["id"]))
        command = "REPLACE INTO t_recommend_log(uid,result,created_at) " \
                  "VALUES (:uid,:recomm_result,now())"
        session.execute(command, {"uid": uid,
                                  "recomm_result": json.dumps(recomm_id_list, ensure_ascii=False)})

        for item in recomm_result:
            command1 = "REPLACE INTO t_user_rec_items(uid,item_id,created_at) " \
                      "VALUES (:uid,:item_id,now())"
            session.execute(command1, {"uid": uid,
                                       "item_id": str(item['id'])})
        session.commit()
        session.close()
        return

    def get_user_rec_items(self, uid):
        command = "SELECT item_id from t_user_rec_items where uid='{}'".format(
            uid)
        item_ids = self.db.read_sql(command)['item_id'].values
        return set(item_ids)
