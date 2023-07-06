#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 同步hive表的存储容量以及记录行数
# author:liuhui@aerozhonghuan.com
import configparser
import os
import datetime
import sys
from store import DbMySQL,DbPostGres
import commands
import threading

max_connections = 5  # 定义最大线程数
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

def getTableAllCapacity(current_day):
    sql = '''
        SELECT
        a.TBL_ID as tbl_id,
        a.TBL_NAME,
        0 as  num_rows,
        0 as  total_size,
        ifnull(e.PARAM_VALUE,f.last_ddltime) as  last_ddl_time
    FROM
        TBLS AS a
        left join table_params e
	    on a.tbl_id=e.tbl_id
        left JOIN DBS as d
        on d.DB_ID = a.DB_ID
		left join (
			select 
			p.tbl_id,
			max(pp.param_value) as last_ddltime
			from `partitions` p
			inner join partition_params pp on p.part_id=pp.part_id 
			where param_key='transient_lastDdlTime' and  p.PART_NAME like '%{current_day}%' 
			group by p.tbl_id
		) f on a.tbl_id=f.tbl_id
    where 
        e.PARAM_KEY='transient_lastDdlTime'
    '''.format(current_day=current_day)

    db_hive = getHiveCloud()
    return db_hive.queryAll(sql)

# 获取全量数据的表大小及记录数
def getTableAllCapacityPool(table):
    pool_sema.acquire()  # 加锁，限制线程数

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    # 获取空间大小
    capacityStr = "hadoop fs -du %s|awk 'BEGIN {total=0} {total+=$1} END {print total}' > /tmp/%s.log" %(table['location'],table['tbl_name'])
    print(capacityStr)
    commands.getoutput(capacityStr)

    tableCapacity = commands.getoutput("head -n 1 /tmp/%s.log" % (table['tbl_name']))

    print('%s-%s' %(table['tbl_name'],tableCapacity))

    storage = '0'

    if tableCapacity:
        storage = tableCapacity

    saveTableCapacity(table['tbl_id'],2,yesterday,0,storage,0)

    pool_sema.release()  # 解锁



# 获取增量数据表的大小及记录数
def getIncTableCapacity(current_day):
    db_hive = getHiveCloud()
    sql='''
    select 
t.tbl_id,
t.tbl_name,
sum(size.total_size) as total_size,
ifnull(sum(rows.num_rows),0) as num_rows,
max(ddl.last_ddltime) as last_ddl_time
from 
tbls as t
left join (
	select 
	p.tbl_id,
	p.part_name,
	pp.param_key,
	pp.param_value as total_size
	from `partitions` p
	inner join partition_params pp on p.part_id=pp.part_id 
	where param_key='totalSize' and  p.PART_NAME like '%{current_day}%'
) size on t.tbl_id=size.tbl_id 
left join (
	select 
	p.tbl_id,
	p.part_name,
	pp.param_key,
	pp.param_value as num_rows
	from `partitions` p
	inner join partition_params pp on p.part_id=pp.part_id 
	where param_key='numRows' and  p.PART_NAME like '%{current_day}%'
) rows on t.tbl_id=rows.tbl_id 
left join (
	select 
	p.tbl_id,
	max(pp.param_value) as last_ddltime
	from `partitions` p
	inner join partition_params pp on p.part_id=pp.part_id 
	where param_key='transient_lastDdlTime' and  p.PART_NAME like '%{current_day}%'
	group by p.tbl_id
) ddl on t.tbl_id=ddl.tbl_id
where size.total_size is not null 
group by t.tbl_id,t.tbl_name 
    '''.format(current_day=current_day)
    return db_hive.queryAll(sql)

# 保存表容量信息
def saveTableCapacity(tbl_id,storage_type,current_day,records,storage,ddl_time):
    db_colud = getDbCloud()
    rowExist = '''
    select id from hive_table_capacity where tbl_id='%s' and storage_type='%s' 
    and calculate_date='%s'
    ''' % (tbl_id,storage_type,current_day)

    resultRow = db_colud.queryRow(rowExist)
    if resultRow:
        updateDict = {
            'storage' : storage,
            'records' : records,
            #'last_ddl_time' : ddl_time
        }
        updateWhere = "tbl_id='%s' and storage_type='%s' and calculate_date='%s' " % (tbl_id,storage_type,current_day)
        db_colud.update('hive_table_capacity',updateDict,updateWhere)
    else:
        insertDict = {
            'tbl_id' : tbl_id,
            'storage' : storage,
            'storage_unit' : 'Byte',
            'records' : records,
            'last_ddl_time' : ddl_time,
            'calculate_date' : current_day,
            'storage_type' : storage_type,
            'create_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        db_colud.insert('hive_table_capacity',insertDict)

# 插入总的存储空间大小
def insertDiskCapacity(current_day):

    (status, result) = commands.getstatusoutput("hadoop fs -df -h > /tmp/hadoop.log")
    print(status)
    db_colud = getDbCloud()

    # print(result)
    if status == 0:
        (status, result) = commands.getstatusoutput("tail -n 1 /tmp/hadoop.log|awk '{print $1,$2,$3,$4,$5,$6,$7,$8}'")
        all_storage = result.split(' ')

        delete_sql = '''
        delete from hive_table_all_storage where calculate_date='%s' 
        ''' % (current_day)
        db_colud.delete(delete_sql)

        insertDict = {
            'file_dir' : all_storage[0],
            'total_size' : str(all_storage[1]) + all_storage[2],
            'used_size' : str(all_storage[3]) + all_storage[4],
            'use_percent' : all_storage[7],
            'calculate_date' : current_day,
            'create_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        db_colud.insert('hive_table_all_storage',insertDict)

def getAllTable():
    """
    获取所有需要统计的表
    :return:
    """
    sql = '''
        select tbl_id,db_name,tbl_name,location from hive_table_info where is_online=1 
    '''
    db_colud = getDbCloud()
    tableInfo = db_colud.queryAll(sql)

    return tableInfo

def getYesterDayAllNum(current_day):
    """
    获取昨天所有的全量行数
    :param current_day:
    :return:
    """
    sql = '''
    select count(id) total from hive_table_capacity where calculate_date='{yesterday}' and storage_type=2
    '''.format(yesterday=current_day)
    db_colud = getDbCloud()
    return db_colud.queryRow(sql)


def thread_run():
    """
    多线程执行获取表占用空间大小，减少程序执行时间
    :return:
    """

    tableInfo = getAllTable()

    thread_list = []
    for table in tableInfo:
        t = threading.Thread(target=getTableAllCapacityPool, args=[table])
        thread_list.append(t)

    for t in thread_list:
        t.start()  # 调用start()方法，开始执行

    for t in thread_list:
        t.join()  # 子线程调用join()方法，使主线程等待子线程运行完毕之后才退出



if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_capacity start' % (start_time))

    if (len(sys.argv) > 1):
        current_day = sys.argv[1]
    else:
        current_day = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    insertDiskCapacity(current_day)

    #全量表,获取最后更新时间
    table_all_capacity = getTableAllCapacity(current_day)
    # 增加判断当天是否已经存在相关数据，存在的话就不用再执行，否则会覆盖表的大小重新计算，页面显示会有差异
    yesterdayNum = getYesterDayAllNum(current_day)
    if yesterdayNum <=0:
        print('全量插入数据')
        for capacity in table_all_capacity:
            saveTableCapacity(capacity['tbl_id'], 2, current_day, capacity['num_rows'], capacity['total_size'],capacity['last_ddl_time'])
    else:
        print('不需要全量插入数据')

    # 增量表，有分区信息
    table_inc_capacity = getIncTableCapacity(current_day)
    for inc_capacity in table_inc_capacity:
        saveTableCapacity(inc_capacity['tbl_id'],1,current_day,inc_capacity['num_rows'],inc_capacity['total_size'],inc_capacity['last_ddl_time'])

    # 全量表，分多个进程进行
    now_hour = datetime.datetime.now().strftime('%H')

    if now_hour != '10':
        thread_run()
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s]-sync_hive_table_capacity end' % (end_time))