#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 同步hive表信息，获取基本信息，分区字段，字段描述
# 更新频率，每小时更新一次
# author:liuhui@aerozhonghuan.com
import configparser
import os
import datetime
import sys
from store import DbMySQL,DbPostGres
import json
import re
import time


# 获取config配置文件
def getDBConfig(section):
    config = configparser.ConfigParser()
    path = os.path.dirname(__file__) + '/config/config.ini'
    config.read(path)
    db_config = {}
    db_config["host"] = config.get(section, "host")
    db_config["user"] = config.get(section, "user")
    db_config["passwd"] = config.get(section, "passwd")
    db_config["port"] = config.getint(section, "port")
    db_config["db"] = config.get(section, "db")
    return db_config

def getDbCloud():
    cloud_37 = getDBConfig('pg_db')
    db_colud = DbPostGres(cloud_37['host'], cloud_37['user'], cloud_37['passwd'], cloud_37['db'],cloud_37['port'])
    return db_colud

def getHiveCloud():
    hive_config = getDBConfig('hive_db')
    db_hive = DbMySQL(hive_config['host'], hive_config['user'], hive_config['passwd'], hive_config['db'])

    return db_hive

def main():
    # 获取所有的hive表信息
    db_hive = getHiveCloud()
    db_cloud = getDbCloud()

    sql = '''
    	select
        t1.tbl_id,
        t1.tbl_name,
        t1.db_id,
        t2.name as db_name,
        t1.tbl_type,
        t1.owner as tbl_owner,
        from_unixtime(t1.create_time) as create_time,
        t3.location,
		1 as is_online,
		now() as update_time,
		'' as offline_time,
		tp.tbl_partition_key as `partition`,
		tc.tbl_comment
        from tbls t1
        left join
        dbs t2
        on t1.db_id = t2.db_id
        left join
        sds t3
        on t1.sd_id = t3.sd_id
		left join (
			select
			tbl_id,
			cast(group_concat(pkey_name SEPARATOR '/') as char) as tbl_partition_key
			from partition_keys 
			group by tbl_id
		) tp on t1.tbl_id=tp.tbl_id
		left join (
			select
			tbl_id,
			param_value as tbl_comment
			from table_params where PARAM_KEY = 'comment'
		) tc on t1.tbl_id=tc.tbl_id
    '''
    tableInfo = db_hive.queryAll(sql)

    tblIdList = []
    for table in tableInfo:
        #print(table)
        sql = '''
            select tbl_id,db_id from hive_table_info where tbl_id='{tbl_id}'
        '''.format(tbl_id=table['tbl_id'])
        tableExist =  db_cloud.queryRow(sql)

        if tableExist:
            updateDict = table.copy()
            updateDict.pop('tbl_id')
            whereStr = "tbl_id='%s'" % (table['tbl_id'])
            db_cloud.update('hive_table_info',updateDict,whereStr)
        else:
            insertDict = table
            db_cloud.insert('hive_table_info',insertDict)

        tblIdList.append(table['tbl_id'])

    tblIdIn = ','.join(tblIdList)

    existIdSql = '''
        select tbl_id,is_online,offline_time from hive_table_info where tbl_id not in ({tblIdIn})
    '''.format(tblIdIn=tblIdIn)
    #print(existIdSql)

    offlineInfo = db_cloud.queryAll(existIdSql)

    # 获取所有的id进行匹配，看看哪些不存在，不存在的说明已经下线了，更新下状态及下线时间
    for offline in offlineInfo:
        updateDict = {}
        updateDict['is_online'] = 0

        print(offline)
        if offline['offline_time'] !='':
            print('tbl_id:%s,已经下线' %(offline['tbl_id']))
        else:
            print('tbl_id:%s,没有下线，更新下线时间'%(offline['tbl_id']))
            updateDict['offline_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        whereStr = "tbl_id='%s'" % (offline['tbl_id'])
        db_cloud.update("hive_table_info",updateDict,whereStr)


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_info start' % (start_time))

    main()

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_info end' % (end_time))