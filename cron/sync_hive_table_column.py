#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 同步hive表的列信息
# author:liuhui@aerozhonghuan.com
import configparser
import os
import datetime
import sys
from store import DbMySQL,DbPostGres

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

# 获取表的列信息
def getHiveColumn():
    sql_hivecolumns = '''
    select
        concat(t1.cd_id,"_",t1.integer_idx) as column_id ,
        t1.cd_id,
        t1.integer_idx,
        t1.column_name,
        t1.type_name,
        t1.comment,
        t3.tbl_id,
        t3.`tbl_name` as table_name,
        t4.db_id,
        t4.`name` as db_name
    from 
        COLUMNS_V2 t1
    join 
        SDS t2 on t1.CD_ID = t2.CD_ID
    JOIN 
        TBLS t3 on t2.SD_ID = t3.SD_ID
    JOIN 
        DBS t4 on t3.DB_ID = t4.DB_ID limit 100
    '''

    return db_hive.queryAll(sql_hivecolumns)


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_column start' % (start_time))

    cloud_37 = getDBConfig('pg_db')
    db_colud = DbPostGres(cloud_37['host'], cloud_37['user'], cloud_37['passwd'], cloud_37['db'],cloud_37['port'])

    hive_config = getDBConfig('hive_db')
    db_hive = DbMySQL(hive_config['host'], hive_config['user'], hive_config['passwd'], hive_config['db'])

    #获取列信息没有就新增，有就修改
    hive_column = getHiveColumn()
    for column in hive_column:
        columnSql = '''
                select cd_id from hive_table_column_info where db_name='%s' and table_name='%s' and column_name='%s' 
                 and tbl_id='%s' order by id desc
        ''' % (column['db_name'], column['table_name'],column['column_name'],column['tbl_id'])
        print(column['tbl_id'],column['column_id'])

        columnExist = db_colud.queryRow(columnSql)

        type_name=''
        if column['type_name'].startswith('array'):
            type_name='array'
        elif column['type_name'].startswith('struct'):
            type_name = 'struct'
        else:
            type_name = column['type_name']

        insertDict = {
            'column_id' : column['column_id'],
            'cd_id' : column['cd_id'],
            'integer_idx' : column['integer_idx'],
            'column_name' : column['column_name'],
            'column_type' : type_name,
            'column_desc' : column['comment'],
            'tbl_id' : column['tbl_id'],
            'table_name' : column['table_name'],
            'db_id' : column['db_id'],
            'db_name' : column['db_name'],
        }
        if columnExist:
            where_str = "tbl_id='%s' and db_name='%s' and table_name='%s' and column_name='%s'" % (column['tbl_id'],column['db_name'], column['table_name'],column['column_name'])
            db_colud.update('hive_table_column_info',insertDict,where_str)
        else:
            insertDict['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_colud.insert('hive_table_column_info',insertDict)

    # 判断列是否有删除，进行删除操作

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_column end' % (end_time))


