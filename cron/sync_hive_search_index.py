#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 构建表和字段的索引，写入到索引表里面，方便查询使用
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

# 获取表里面列的字段和列的描述内容
def getTableField(table_id):
    sql = '''select c.table_name,  array_to_string(array_agg(c.column_name),',') column_names,
					array_to_string(array_agg(m.column_desc_maintain),',') column_content
            from hive_table_column_info  c 
            inner join hive_column_maintain m 
            on c.db_name=m.db_name and c.table_name=m.table_name and c.integer_idx=m.column_idx
            where c.tbl_id='%s' group by c.table_name
    ''' % (table_id)
    table_field =  db_mysql.queryRow(sql)
    #print(type(table_field))
    if table_field is None or table_field == '':
        table_field = {}
        table_field['column_names'] = ''
        table_field['column_content'] = ''
    return table_field


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_search_index start' % (start_time))

    cloud_37 = getDBConfig('pg_db')
    db_mysql = DbPostGres(cloud_37['host'], cloud_37['user'], cloud_37['passwd'], cloud_37['db'],cloud_37['port'])

    #db_mysql.selectDb('test')

    sql = '''
        select t.tbl_id,t.tbl_name,t.db_id,t.db_name,t.tbl_type,t.tbl_comment,t.is_online,m.table_desc_maintain 
        from hive_table_info t 
		left join hive_table_maintain m on t.tbl_name=m.table_name and t.db_name=m.db_name
    '''
    table_all = db_mysql.queryAll(sql)

    for t in table_all:
        existSql = '''
        select id from hive_search_index where db_id='%s' and table_id='%s'
        ''' % (t['db_id'],t['tbl_id'])

        indexExist = db_mysql.queryRow(existSql)

        table_name_split = t['tbl_name'].replace('_', ' ')
        # 获取表的列字段及描述，将多列和描述放到一个字段里面
        table_field = getTableField(t['tbl_id'])
        insert_dict = {
            'db_id' : t['db_id'],
            'db_name' : t['db_name'],
            'table_id' : t['tbl_id'],
            'table_name' : t['tbl_name'],
            'table_name_split' : table_name_split,
            'is_online' : t['is_online'],
            'column_names' : table_field['column_names'] ,
            'column_names_split' : table_field['column_names'].replace('_',' '),
            'table_content' : t['table_desc_maintain'],
            'column_content' : table_field['column_content'],
            'table_sort_priority' : 0,
        }
        # 存在的话就更新，不存在的话就插入新的数据
        if indexExist:
            where_str = "db_id='%s' and table_id='%s'" % (t['db_id'],t['tbl_id'])
            db_mysql.update('hive_search_index',insert_dict,where_str)

        else:
            insert_dict['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_mysql.insert('hive_search_index',insert_dict)

        #print(t['tbl_id'], t['tbl_name'])

    #更新索引数据
    sql = '''
        select index_id,count(id) cnt from hive_search_log 
        where date(create_time) > (now()-interval '60d')::date
        group by index_id
    '''
    indexInfo = db_mysql.queryAll(sql)
    for index in indexInfo:
        updateDict = {
            'table_sort_priority' : index['cnt']
        }
        where_str="id='%s'" % (index['index_id'])
        db_mysql.update('hive_search_index', updateDict, where_str)

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_search_index end' % (end_time))





