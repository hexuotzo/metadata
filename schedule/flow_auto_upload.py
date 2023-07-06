#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 构建azkaban flow文件生成,并自动上传
# author:liuhui@aerozhonghuan.com
import os
import datetime
import sys
import subprocess
import time
import requests
import re

from schedule.models import Task,Project,TaskDepend

class MyTask():
    def __init__(self, project_id, project_name,frequency,task_identification,execute_command):
        self.project_id = project_id
        self.project_name = project_name
        self.frequency = frequency
        self.task_identification = task_identification
        self.execute_command = execute_command



# 根据调度频率获取所有的任务
def getTaskByFrequency(frequency, project_id):
    sql = '''
        select t.id,t.project_id, p.project_name, t.task_identification,t.execute_command,t.frequency from schedule_task t 
        left join schedule_project p on t.project_id=p.id
        where t.status=1 and t.task_type=1 and t.frequency='%s' and t.project_id='%s'
    ''' % (frequency, project_id)
    #print(sql)

    return Task.objects.raw(sql)


# 根据task_id获取依赖任务
def getDepends(task_id, project_id, frequency, dependType):
    if dependType == 1:
        sql = '''
            select d.id, st.task_identification from schedule_task_depend d
            left join schedule_task st on d.parent_task_id=st.id
            where d.task_id='%s' and st.project_id='%s' and st.frequency='%s'
        ''' % (task_id, project_id, frequency)
    else:
        sql = '''
            select d.id, st.task_identification from schedule_task_depend d
            left join schedule_task st on d.parent_task_id=st.id
            where d.task_id='%s' and (st.project_id!='%s' or st.frequency!='%s')
        ''' % (task_id, project_id, frequency)
    dependTask = TaskDepend.objects.raw(sql)
    dependList = []
    for depend in dependTask:
        dependList.append(depend.task_identification)

    return dependList


# 从依赖字符串里面过滤掉是内部依赖还是外部依赖
def getDependsByDependStr(project_id, frequency, dependType=1,dependStr=''):
    dependList = []

    if dependStr:
        dependInStr = " and st.id in (%s)" % (dependStr)

        if dependType == 1:
            sql = '''
                select st.id,st.task_identification from schedule_task st
                where st.project_id='%s' and st.frequency='%s' %s
            ''' % (project_id, frequency,dependInStr)
        else:
            sql = '''
                select st.id,st.task_identification from schedule_task st
                where (st.project_id!='%s' or st.frequency!='%s') %s
            ''' % (project_id, frequency,dependInStr)
        dependInsideTask = TaskDepend.objects.raw(sql)

        for depend in dependInsideTask:
            dependList.append(depend.task_identification)

    return dependList



# 根据执行频率获取名称
def getFrequencyName(frequency):
    frequencyDict = {
        '1': 'hour',
        '2': 'day',
        '3': 'week',
        '4': 'month',
        '5': 'quator',
        '6': 'year',
    }

    return frequencyDict[str(frequency)]

# 写入一行到文件
def writeLineToFile(fileName, str):
    file = open(fileName, "a")
    file.write(str)
    file.close()


# 根据不同频率的任务写入对应文件中
def writeToFlow(frequency, task, dependTask,checkTag=[]):
    frequencyName = getFrequencyName(frequency)
    fileName = 'schedule_%s.flow' % (frequencyName)
    print(fileName)

    fileDir = getFileDir(task.project_name)
    fileFullName = fileDir + fileName

    # 判断文件是否存在，不存在的话先插入全局变量，存在的话就插入节点信息
    task_str = ''
    if not os.path.exists(fileFullName):
        globalStr = '''config:
    spark_online: spark-sql --master yarn --queue online --executor-memory 3G
    hive: hive -hiveconf hive.exec.compress.intermediate=true -hiveconf hive.exec.compress.output=true -hiveconf tez.queue.name=online
    year: ${azkaban.flow.start.year}
    month: ${azkaban.flow.start.month}
    day: ${azkaban.flow.start.day}
    time: $(new("org.joda.time.DateTime").minusDays(1).toString("yyyy-MM-dd HH:mm:ss"))

    # hdfs 标记路径
    hdfs_target: /home/hdfs/status

    # 代码路径
    cur_dir: /project/warehouse_20210430/etl/dwd_test

    # 当天
    C_DATE: $(new("org.joda.time.DateTime").toString("yyyy-MM-dd"))

    # 昨天，通常为t-1跑批日期
    SDATE: $(new("org.joda.time.DateTime").minusDays(1).toString("yyyy-MM-dd"))

    # 前天，t-2 日期
    YT_DATE: $(new("org.joda.time.DateTime").minusDays(2).toString("yyyy-MM-dd"))

    retries: 10
    retry.backoff: 1200000

nodes:'''
        writeLineToFile(fileFullName, globalStr)
    # 写入node
    taskStr = '''
  - name: {taskName}
    type: command'''.format(taskName=task.task_identification)
    writeLineToFile(fileFullName, taskStr)
    # 写入依赖
    if dependTask:
        dependHead = '''
    dependsOn:'''
        writeLineToFile(fileFullName, dependHead)

        for depend in dependTask:
            dependTask = '''
        - {depend}'''.format(depend=depend)
            writeLineToFile(fileFullName, dependTask)

    # 写入执行命令
    configStr = '''
    config:'''
    writeLineToFile(fileFullName, configStr)

    #commandList = task.execute_command.split("\r\n").split("@")
    commandList = re.split("[\r\n|@]", task.execute_command)

    # if not checkTag:
    #     checkTag = getDepends(task.id, task.project_id, task.frequency, dependType=2)

    if checkTag:
        checkTagSplit = ','.join(checkTag)
        azcheckStr = '''
      command: az_check_tag %s ${SDATE} hdfs ${hdfs_target}''' % (checkTagSplit)
        writeLineToFile(fileFullName, azcheckStr)

    for key, command in enumerate(commandList):
        if not checkTag and key == 0:
            commandStr = '''
      command: {command}'''.format(command=command)
            writeLineToFile(fileFullName, commandStr)
        else:
            if command:
                commandStr = '''
      command.{key}: {command}'''.format(key=key, command=command)
                writeLineToFile(fileFullName, commandStr)

    writeLineToFile(fileFullName, "\n")

def deldir(dir):
    '''
    递归删除目录下的文件
    :param dir:
    :return:
    '''
    if not os.path.exists(dir):
        return False
    if os.path.isfile(dir):
        os.remove(dir)
        return
    for i in os.listdir(dir):
        t = os.path.join(dir, i)
        if os.path.isdir(t):
            deldir(t)  # 重新调用次方法
        else:
            os.unlink(t)
    os.removedirs(dir)  # 递归删除目录下面的空文件夹


# 获取项目的位置
def getFileDir(project_name):
    currentDay = datetime.datetime.now().strftime("%Y%m%d")
    fileDir = '/tmp/%s_%s/' % (project_name, currentDay)
    return fileDir


def initFileInfo(project_id):
    '''
    初始化要生成的文件相关信息
    :return:
    '''

    fileDir = getFileDir(project_id)
    # 1.删除文件
    deldir(fileDir)

    print(fileDir)
    if not os.path.exists(fileDir):
        os.mkdir(fileDir)
        print('mkdir %s' % (fileDir))
    else:
        print('dir %s is exist' % (fileDir))

    # 2.创建.project文件
    writeLineToFile(fileDir + 'a3_data.project', 'azkaban-flow-version: 2.0')
    # 3.创建 readme.txt文件
    writeLineToFile(fileDir + 'README.txt', '# this file is auto create')

# 获取所有的project
def getProjectInfo(project_id):
    sql = '''
    select  t.id,t.project_id,p.project_name
    from schedule_task t inner join schedule_project p on t.project_id=p.id
    where t.project_id='%s'
    group by t.project_id
    ''' % (project_id)

    return Task.objects.raw(sql)

def get_session_id():
    '''
        azkaban认证接口
        curl -k -X POST --data "action=login&username=azkaban&password=azkaban" http://192.168.134.207:8081/
    '''
    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }
    AZ_URI = 'http://192.168.134.207:8081/'
    user = 'azkaban'
    passwd = 'azkaban'
    body = {
        'action':'login',
        'username':user,
        'password':passwd
    }
    rc = requests.post(AZ_URI, headers=HEADERS, data=body)
    # {u'status': u'success', u'session.id': u'ea318ae3-57fc-4702-877e-597b5e46b292'}
    session_id = rc.json()['session.id']
    return session_id

def auto_upload_zk_file(projectName,azFileDir):

    """
    自动压缩azkaban的目录文件生成zip,再进行上传
    azkaban接口文档：https://azkaban.github.io/azkaban/docs/latest/#api-upload-a-project-zip
    :param projectName: 项目名称
    :param azFileDir: 需要进行zip压缩的文件路径
    :return:
    """
    returnDict = {
        'succ' : False,
        'msg' : ''
    }
    # 判断文件目录是否存在,存在的话就进行zip压缩
    zipFile = ''
    if os.path.exists(azFileDir):
        zipFile = '/tmp/file_%s_%s.zip' % (projectName,int(time.time()))
        execShell = '''zip -r {zipFile} {azFileDir}'''.format(zipFile=zipFile,azFileDir=azFileDir)
        print(execShell)
        (status, result) = subprocess.getstatusoutput(execShell)
        print(status,result)
        if status != 0:
            returnDict['msg'] = 'zip file error'
            return returnDict

    else:
        returnDict['msg'] = 'file dir:%s is not exist' % (azFileDir)
        return returnDict

    # 判断文件是否存在
    if not os.path.exists(zipFile):
        returnDict['msg'] ='zipFile:%s is not exist' % (zipFile)
        return returnDict

    # 获取session id
    sessionId = get_session_id()

    uploadUrl = 'http://192.168.134.207:8081/manager'

    headers = {
        #'Content-Type': 'multipart/form-data',
    }

    #projectName = 'lh_az_test'
    fileName = os.path.basename(zipFile)

    files = {
        'file': (fileName, open(zipFile, 'rb'),'application/zip'),
    }

    data = {
        'session.id': (None, sessionId),
        'ajax': (None, 'upload'),
        'project': (None, projectName),
    }

    response = requests.post(url=uploadUrl,headers=headers, files=files, data=data,verify=False)
    #print(response.text)
    # 判断是否成功上次了tar包，如果没有上传成功，发邮件告知
    if response.status_code == 200:
        jsonDict = response.json()

        if 'error' in jsonDict.keys():
            returnDict = "[%s]-上传tar包失败，error:%s" % (datetime.datetime.now(),jsonDict['error'])
            return returnDict
        else:
            returnDict['succ'] = True
            return returnDict
    else:
        returnDict['msg'] = '请求http:%s 接口异常'%(uploadUrl)
        return returnDict


def flow_generate(project_id):
    projectInfo = getProjectInfo(project_id)

    for project in projectInfo:
        initFileInfo(project.project_name)

        # 获取需要构建的所有任务，根据调度频率写入不同的文件
        for frequency in range(1, 7):
            taskInfo = getTaskByFrequency(frequency, project_id)

            if taskInfo:
                for task in taskInfo:
                    dependTask = getDepends(task.id, task.project_id, task.frequency, dependType=1)
                    print('write: project-%s,task-%s,frequency-%s' % (task.project_id, task.id, frequency))
                    writeToFlow(frequency, task, dependTask)

    #return task

def flow_generate_tmp(project_id,task_identification,frequency,execute_command,depend):
    """
    生成临时的flow job，数据直接从页面获取
    :param project_id:
    :param task_identification:
    :param frequency:
    :param execute_command:
    :param depend:
    :return:
    """
    projectInfo = Project.objects.get(pk=project_id)
    taskInfo = MyTask(project_id=project_id,project_name=projectInfo.project_name,frequency=frequency,task_identification=task_identification,execute_command=execute_command)

    dependList = getDependsByDependStr(project_id,frequency,dependType=1,dependStr=depend)
    checkTagList = getDependsByDependStr(project_id,frequency,dependType=2,dependStr=depend)
    print(dependList)
    print(checkTagList)
    writeToFlow(frequency,taskInfo,dependList,checkTagList)



def flow_upload(project_id):
    """
    flow 自动上传
    :return:
    """
    projectInfo = getProjectInfo(project_id)
    for project in projectInfo:
        fileDir = getFileDir(project.project_name)

        azFile = 'lh_az_test'
        return auto_upload_zk_file(azFile, fileDir)

def flow_generate_and_upload(project_id,task_identification,frequency,execute_command,depend):
    """
    flow 生成并上传
    :param project_id:
    :return:
    """
    flow_generate(project_id)

    flow_generate_tmp(project_id,task_identification,frequency,execute_command,depend=depend)
    uploadReturn = flow_upload(project_id)

    return uploadReturn


