#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 同步hive扩展信息，包括存储压缩格式，最后更新时间
# 更新频率，每天一次，不需要频繁更新
# author:liuhui@aerozhonghuan.com
import configparser
import os
import datetime
import sys
from store import DbMySQL,DbPostGres
import json
import commands
import re
import time
import threading

max_connections = 3  # 定义最大线程数
pool_sema = threading.BoundedSemaphore(max_connections)  # 或使用Semaphore方法


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


def getAllTable():
    """
    获取所有需要统计的表
    :return:
    """
    sql = '''
        select tbl_id,db_name,tbl_name,create_time from hive_table_info where is_online=1 
    '''
    db_colud = getDbCloud()
    tableInfo = db_colud.queryAll(sql)

    return tableInfo


def thread_main(tableInfo):
    pool_sema.acquire()  # 加锁，限制线程数

    db_colud = getDbCloud()
    db_hive = getHiveCloud()

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    table = tableInfo
    #for table in tableInfo:
    print(table['db_name'],table['tbl_name'])

    tableStructFile = '/tmp/table/{db_name}_{tbl_name}.log'.format(db_name=table['db_name'],tbl_name=table['tbl_name'])
    if not os.path.exists(tableStructFile):
        shellStr = "mkdir /tmp/table;hive -e 'show create table {db_name}.{tbl_name}' > /tmp/table/{db_name}_{tbl_name}.log".format(db_name=table['db_name'],tbl_name=table['tbl_name'])
        #print(shellStr)
        commands.getoutput(shellStr)

    if os.path.exists(tableStructFile):
        # 正则匹配获取压缩存储格式，最后更新时间
        storage = commands.getoutput("cat /tmp/table/{db_name}_{tbl_name}.log | grep -aE 'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat|org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat|org.apache.hadoop.mapred.SequenceFileInputFormat|org.apache.hadoop.mapred.TextInputFormat|org.apache.hudi.hadoop.HoodieParquetInputFormat' ".format(db_name=table['db_name'],tbl_name=table['tbl_name']))
        #print(storage)

        if storage and (storage.find('OrcInputFormat') >= 0):
            storage_str = 'Orc'
        elif storage and (storage.find('MapredParquetInputFormat') >= 0):
            storage_str = 'Parquet'
        elif storage and (storage.find('SequenceFileInputFormat') >= 0):
            storage_str = 'SequenceFile'
        elif storage and (storage.find('TextInputFormat') >= 0):
            storage_str = 'Text'
        elif storage and (storage.find('HoodieParquetInputFormat') >= 0):
            storage_str = 'HoodieParquet'
        elif storage and (storage.find('AVRO') >= 0):
            storage_str = 'AVRO'
        else:
            storage_str = ''

        #print(storage_str)

        compression = commands.getoutput("cat /tmp/table/{db_name}_{tbl_name}.log| grep -a 'compression' ".format(db_name=table['db_name'],tbl_name=table['tbl_name']))
        if compression and compression.find('SNAPPY') >=0:
            compression_str = 'SNAPPY'
        elif compression and compression.find('GZIP') >=0:
            compression_str = 'GZIP'
        elif compression and compression.find('BZIP2') >=0:
            compression_str = 'BZIP2'
        elif compression and compression.find('lzo') >=0:
            compression_str = 'LZO'
        else:
            compression_str = ''

        #print(compression_str)

        # 获取ddltime
        # 获取逻辑，先获取partitions表的数据，没有的话再获取全量表的数据，

        paramSql = '''
                    select 
                    p.tbl_id,
                    p.part_name,
                    pp.param_key,
                    pp.param_value as last_ddltime,
                    FROM_UNIXTIME(pp.param_value,'%Y-%m-%d %H:%i:%S') ddl_time
                    from `partitions` p
                    inner join partition_params pp on p.part_id=pp.part_id 
                    where param_key='transient_lastDdlTime' and p.tbl_id='{tbl_id}' order by pp.param_value desc limit 1;
                    '''.format(tbl_id=table['tbl_id'])
        paramInfo = db_hive.queryRow(paramSql)
        if paramInfo:
            ddlTimeStr = paramInfo['ddl_time']
        else:
            ddlSql = '''select tbl_id,FROM_UNIXTIME(max(param_value),'%Y-%m-%d %H:%i:%S') as ddl_time from table_params 
                        where tbl_id='{tbl_id}' and param_key in ('last_modified_time','transient_lastDdlTime')
                    '''.format(tbl_id=table['tbl_id'])
            ddlInfo = db_hive.queryRow(ddlSql)
            if ddlInfo:
                ddlTimeStr = ddlInfo['ddl_time']
            else:
                ddlTimeStr = table['create_time']

        print("db_name:%s,table_name:%s,ddl_time:%s"%(table['db_name'],table['tbl_name'],ddlTimeStr))

        existSql = '''
            select id,tbl_id from hive_table_extend where tbl_id='{tbl_id}'
        '''.format(tbl_id=table['tbl_id'])
        extendInfo = db_colud.queryRow(existSql)

        if extendInfo:
            updateDict = {
                'storage_format' : storage_str,
                'compression' : compression_str,
                'last_ddl_time' : ddlTimeStr,
            }
            whereStr = "tbl_id='%s' " % (table['tbl_id'])
            db_colud.update("hive_table_extend",updateDict,whereStr)
        else:
            insertDict = {
                'tbl_id' : table['tbl_id'],
                'storage_format': storage_str,
                'compression': compression_str,
                'last_ddl_time': ddlTimeStr,
                'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            db_colud.insert("hive_table_extend",insertDict)

    else:
        print('{db_name}.{tbl_name} show  create table error '.format(db_name=table['db_name'],tbl_name=table['tbl_name']))

    pool_sema.release()  # 解锁

def thread_run():
    """
    多线程执行，减少程序执行时间
    :return:
    """

    tableInfo = getAllTable()

    thread_list = []
    for table in tableInfo:
        t = threading.Thread(target=thread_main, args=[table])
        thread_list.append(t)

    for t in thread_list:
        t.start()  # 调用start()方法，开始执行

    for t in thread_list:
        t.join()  # 子线程调用join()方法，使主线程等待子线程运行完毕之后才退出


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_extend start' % (start_time))

    now_hour = datetime.datetime.now().strftime('%H')

    if now_hour == '10':
        thread_run()

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_extend end' % (end_time))

