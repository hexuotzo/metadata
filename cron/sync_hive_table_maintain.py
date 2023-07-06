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

# 获取表的描述信息
def getHiveTableDesc():
    sql = '''
        select db_name,tbl_name,tbl_comment from hive_table_info
    '''

    return db_colud.queryAll(sql)

# 获取列的描述信息
def getHiveTableColumnDesc():
    sql = '''
        select table_name,db_name,tbl_id,column_desc,integer_idx as column_idx from hive_table_column_info
    '''

    return db_colud.queryAll(sql)

if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_maintain start' % (start_time))


    cloud_37 = getDBConfig('pg_db')
    db_colud = DbPostGres(cloud_37['host'], cloud_37['user'], cloud_37['passwd'], cloud_37['db'],cloud_37['port'])


    #同步表名信息到维护表中，不做修改
    hive_table = getHiveTableDesc()
    for table in hive_table:
        sql_exist = '''
            select db_name,table_name from hive_table_maintain 
            where db_name='%s' and table_name='%s'
        ''' % (table['db_name'],table['tbl_name'])

        table_info = db_colud.queryRow(sql_exist)
        if table_info:
            pass
        else:
            insert_dict = {
                'db_name': table['db_name'],
                'table_name' : table['tbl_name'],
                'table_desc_maintain' : table['tbl_comment'],
                'create_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(table['db_name'],table['tbl_name'])
            db_colud.insert('hive_table_maintain',insert_dict)
    #同步列名信息到维护表中，不做修改
    hive_column = getHiveTableColumnDesc()
    for column in hive_column:
        sql_exist = '''
            select db_name,table_name from hive_column_maintain
            where db_name = '%s' and table_name='%s' and column_idx='%s'
        ''' % (column['db_name'],column['table_name'],column['column_idx'])
        column_info = db_colud.queryRow(sql_exist)
        if column_info:
            pass
        else:
            insert_dict = {
                'db_name' : column['db_name'],
                'table_name' : column['table_name'],
                'column_idx' : column['column_idx'],
                'column_desc_maintain' : column['column_desc'],
                'create_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(column['db_name'],column['table_name'],column['column_idx'])
            db_colud.insert('hive_column_maintain',insert_dict)

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_maintain end' % (end_time))


