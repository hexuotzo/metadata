#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from psycopg2 import extras

class DbPostGres:

    def __init__(self,DB_HOST,DB_USER,DB_PASS,DB_NAME,DB_PORT):
        try:
            self.conn = psycopg2.connect(host=DB_HOST,
                                        port=DB_PORT,
                                        user=DB_USER,
                                        password=DB_PASS,
                                        database=DB_NAME)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except psycopg2.Error as e:
            print("postgres connect Error  %s" % (e))

    #执行sql
    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except psycopg2.Error as e:
            print("Mysql Error:%s\nSQL:%s" % (e, sql))

    def queryRow(self, sql):
        """
        查询一行数据，返回字典格式的数据
        调用方式 query_row(sql)
        :param sql: 查询sql
        :return: {'key1':value1,'key2':value2}
        """
        self.query(sql)
        result = self.cur.fetchone()

        if result:
            return dict(result)

        return result

    def queryAll(self, sql):
        """
        查询所有数据，返回列表嵌套字典格式的数据
        调用方式 query_all(sql)
        :param sql: 查询sql
        :return: [{'key1':value1,'key2':value2},{'key1':value1,'key2':value2}]
        """
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        result = []
        if rows:
            for row in rows:
                new_row = dict(row)
                for j in new_row:
                    if new_row[j] == None:
                        new_row[j] = ''
                result.append(new_row)

        return result

    # 调用方式 insert('table','{key1:val1,key2:val2}',False)
    def insert(self, p_table_name, p_data, replace=False):
        """
        向指定表中插入一条数据
        调用方式 insert('table','{key1:val1,key2:val2}',False)
        :param p_table_name: 表名
        :param p_data: 表数据 字典格式{'field1':'val','field2':'val'}
        :param replace: 是否替换
        :return: 插入表的最后新增id
        """
        p_data_copy = p_data.copy()
        formatKeys = ''
        formatValues = ''
        for pkey, pval in p_data_copy.items():
            formatValues += "'" + str(pval) + "',"
            formatKeys += "%s," % (pkey)
        key = formatKeys.rstrip(',')
        value = formatValues.rstrip(',')
        if replace:
            insert = "REPLACE"
        else:
            insert = "INSERT"
        real_sql = insert + " INTO " + p_table_name + " (" + key + ") VALUES (" + value + ")"
        self.query(real_sql)
        self.commit()

        return self.cur.lastrowid

    def update(self, p_table_name, p_data, where):
        '''
        更新数据
        使用方式 update('user_label_list',{'label_desc':'aaaa'},"id=1")
        :param p_table_name: 表名
        :param p_data: 要更新的列 字典格式 {'key1':'val1','key2':'val2'}
        :param where: where条件
        :return: 修改的记录条数
        '''
        p_data_copy = p_data.copy()
        for key in p_data_copy:
            p_data_copy[key] = "" + key + "='" + str(p_data_copy[key]) + "'"
        value = ','.join(p_data_copy.values())

        real_sql = "UPDATE " + p_table_name + " SET " + value + " WHERE " + where

        self.query(real_sql)
        self.commit()

        return self.cur.rowcount

    # 直接执行sql删除记录
    # delete("delete from table where field=1")
    def delete(self, sql):
        self.query(sql)
        self.commit()
        return self.rowcount()

    # 获取最后插入的id
    def getLastInsertId(self):
        return self.cur.lastrowid

    # 获取行记录
    def rowcount(self):
        return self.cur.rowcount

    # 提交
    def commit(self):
        self.conn.commit()

    # 关闭连接
    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_HOST = "10.51.26.208"
    DB_PORT = "5432"

    pg_db = DbPostGres(DB_HOST,DB_USER,DB_PASS,DB_NAME,DB_PORT)
    row = pg_db.queryRow("select * from dk_data_list limit 10")
    print(row)
    print('-----------------------------------------------------')
    # rows = pg_db.queryAll("select * from dk_data_list limit 5")
    # print(rows)

    insert_data={
        'db_name':'dwd',
        'table_name':'dwd_video_metadata_pdi',
        'table_desc_maintain':'视频元数据表',
        'usage_desc':'使用信息',
        'create_time':'2023-03-15 11:24:33'
    }
    #res = pg_db.insert("hive_table_maintain",insert_data)
    #print(res)
    update_data = {
        'usage_desc':'使用信息2'
    }
    where = "id=1"
    res = pg_db.update("hive_table_maintain",update_data,where)
    print(res)
