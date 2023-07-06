# coding: utf-8
# author: liuhui10501@navinfo.com
# mysql链接类，方便做查询，写入，删除
import pymysql


class DbMySQL:
    def __init__(self, host,user,passwd,db,port=3306,charset='utf8'):
        try:
            self.conn = pymysql.connect(host=host,
                                        port=port,
                                        user=user,
                                        passwd=passwd,
                                        db=db,
                                        charset=charset)
            self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 选择库名
    def selectDb(self, db):
        try:
            self.conn.select_db(db)
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    #执行sql
    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except pymysql.Error as e:
            print("Mysql Error:%s\nSQL:%s" % (e, sql))

    #只查找一条记录
    # 返回字典格式{key1:val1,key2:val2}
    def queryRow(self, sql):
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.query(sql)
        result = self.cur.fetchone()
        # d = {}
        # for i,v in result.iteritems():
        #     d[i] = str(v)

        return result

    # 查找全部记录
    # 返回格式[{key1:val1,key2:val2},{key1:val1,key2:val2}]
    def queryAll(self, sql):
        self.cur = self.conn.cursor()
        self.query(sql)
        result = self.cur.fetchall()
        desc = self.cur.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                theval = str(inv[i])
                if theval == 'None':
                    _d[desc[i][0]] = ''
                else:
                    _d[desc[i][0]] = theval
            d.append(_d)
        return d

    # 插入信息
    # 调用方式 insert('table','{key1:val1,key2:val2}',False)
    def insert(self, p_table_name, p_data, replace=False):
        p_data_copy = p_data.copy()
        formatKey = ''
        for key in p_data_copy:
            p_data_copy[key] = "'" + str(p_data_copy[key]) + "'"
            formatKey += "`%s`," % (key)
        #key = ','.join(p_data_copy.keys())
        key = formatKey.rstrip(',')
        value = ','.join(p_data_copy.values())
        if replace:
            insert = "REPLACE"
        else:
            insert = "INSERT"
        real_sql = insert + " INTO " + p_table_name + " (" + key + ") VALUES (" + value + ")"
        self.query(real_sql)
        self.commit()
        return self.getLastInsertId()

    # 跟新表数据
    # 使用方法 update('tablename','{key1:val1,key2:val2}','id=1'}
    def update(self, p_table_name, p_data, where):
        p_data_copy = p_data.copy()
        for key in p_data_copy:
            p_data_copy[key] = "`"+key + "`='" + str(p_data_copy[key]) + "'"
        value = ','.join(p_data_copy.values())

        real_sql = "UPDATE " + p_table_name + " SET " + value + " WHERE " + where

        self.query(real_sql)
        self.commit()
        return self.rowcount()

    # 直接执行sql删除记录
    # delete("delete from table where field=1")
    def delete(self, sql):
        self.query(sql)
        self.commit()
        return self.rowcount()

    # 执行sql
    def executeSql(self, sql):
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

