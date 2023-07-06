# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cgi
from django.db import models
#项目表
class Project(models.Model):
    #id = models.IntegerField(primary_key=True)
    project_name = models.CharField('项目名称',max_length=50, blank=False, unique=True, null=False)
    project_desc = models.CharField('项目描述',max_length=200, blank=False,  null=False)

    user_name = models.CharField('创建人',max_length=30, blank=False,null=False)
    update_user_name = models.CharField('修改人',max_length=30, blank=False, null=False)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        managed = False
        db_table = 'schedule_project'
        verbose_name ='项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.project_name

# 项目成员
class ProjectUser(models.Model):
    id = models.IntegerField(primary_key=True)

    project_id = models.IntegerField('项目id', blank=False,null=False)
    user_id = models.IntegerField('用户id', blank=False,null=False)

    class Meta:
        managed = False
        db_table = 'schedule_project_user'
        verbose_name ='项目成员'
        verbose_name_plural = '项目成员'

# 任务表
class Task(models.Model):
    frequency_choice = (
        (1,'小时'),
        (2,'天'),
        (3,'周'),
        (4,'月'),
        (5,'季度'),
        (6,'年')
    )
    task_type_choice = (
        (1,'离线任务'),
        (2,'实时任务')
    )
    status_choice = (
        (0,'下线'),
        (1,'上线')
    )
    id = models.AutoField(primary_key=True)

    #project_id = models.IntegerField('项目id', blank=False,null=False)
    project_id = models.ForeignKey("Project",db_column='project_id',on_delete=models.CASCADE,verbose_name="项目名称")

    task_identification = models.CharField('任务标识',max_length=100, blank=False,null=False)
    task_name = models.CharField('任务名称',max_length=100, blank=False,null=False)
    task_desc = models.CharField('任务描述',max_length=200, blank=False,null=False)
    owner_name = models.CharField('责任人',max_length=50, blank=False,null=False)
    frequency = models.IntegerField('调度频率', choices=frequency_choice,null=False)
    execute_command = models.CharField('执行命令',max_length=1000, blank=False,null=False)

    task_type = models.IntegerField('任务类型', choices=task_type_choice,null=False)
    status = models.IntegerField('状态', choices=status_choice,null=False)

    user_id = models.IntegerField('用户id', blank=False,null=False)
    update_user_id = models.IntegerField('修改用户id', blank=False,null=False)
    create_time = models.DateTimeField('上线时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    import_type = models.IntegerField('导入类型', blank=False,null=False)

    class Meta:
        managed = False
        db_table = 'schedule_task'
        verbose_name ='任务'
        verbose_name_plural = '任务'


#任务依赖表
class TaskDepend(models.Model):

    task_id = models.IntegerField('任务id', blank=False,null=False)
    parent_task_id = models.IntegerField('依赖父级id', blank=False,null=False)
    create_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'schedule_task_depend'
        verbose_name ='任务依赖表'
        verbose_name_plural = '任务依赖表'

        unique_together = ('task_id', 'parent_task_id',)

#任务日志表
class TaskLog(models.Model):
    id = models.IntegerField(primary_key=True)

    task_id = models.IntegerField('任务id', blank=False,null=False)

    edit_before = models.TextField('修改前数据', blank=False,null=False)
    edit_before_user = models.CharField('修改前用户', max_length=50, blank=False,null=False)

    edit_after = models.TextField('修改后数据', blank=False,null=False)
    edit_after_user = models.CharField('修改后用户', max_length=50, blank=False,null=False)

    create_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'schedule_task_log'
        verbose_name ='任务修改日志表'
        verbose_name_plural = '任务修改日志表'

#任务监控表
class MonitorOff(models.Model):

    monitor_type_choice = (
        (1,'离线'),
        (2,'实时')
    )
    monitor_mode_choice = (
        (1,'完成时间监控'),
        (2,'运行时长监控'),
        (3,'kafka积压量监控'),
        (4,'任务活性监控'),
    )

    from_type_choice = (
        (1, 'streamx任务'),
        (2, '后台手动任务'),
    )

    status_type_choice = (
        (1, '上线'),
        (2, '下线'),
    )

    id = models.AutoField(primary_key=True)

    monitor_type = models.IntegerField('监控类型', choices=monitor_type_choice,null=False)
    task_identification = models.CharField('任务标识',max_length=100, blank=False,null=False)
    monitor_name = models.CharField('任务名称',max_length=100, blank=False,null=False)
    owner_name = models.CharField('责任人',max_length=50, blank=False,null=False)
    monitor_mode = models.IntegerField('监控方式',choices=monitor_mode_choice,null=False)
    finish_time = models.CharField('任务完成时间',max_length=50, blank=False,null=False)
    run_time = models.CharField('任务运行时长',max_length=50, blank=False,null=False)
    monitor_value = models.CharField('监控值',max_length=500, blank=False,null=False)
    is_warning_custom = models.IntegerField('是否自定义报警', blank=False,null=False)

    task_from = models.IntegerField('任务来源', choices=from_type_choice,null=False)
    warning_send_time = models.CharField('报警发送时间',max_length=50, null=False)
    warning_type = models.IntegerField('报警方式', blank=False,null=False)
    user_id = models.IntegerField('创建人', blank=False,null=False)

    status = models.IntegerField('状态', choices=status_type_choice,null=False)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        managed = False
        db_table = 'schedule_task_monitor'
        verbose_name ='任务监控'
        verbose_name_plural = '任务监控'

#监控任务接收人表
class MonitorReceiver(models.Model):
    id = models.AutoField(primary_key=True)

    monitor_id = models.IntegerField('监控id', blank=False,null=False)
    user_type = models.IntegerField('用户类型', blank=False,null=False)
    user_id = models.IntegerField('用户id', blank=False,null=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'schedule_monitor_receiver'
        verbose_name ='监控任务接收人表'
        verbose_name_plural = '监控任务接收人表'

# 实时任务监控
class MonitorReal(models.Model):

    class Meta:
        managed = False
        db_table = 'schedule_task_monitor'
        verbose_name = '实时任务监控'
        verbose_name_plural = '实时任务监控'

# streamx任务表
class StreamxTask(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField('任务名称',max_length=100, null=False)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'schedule_streamx_task'
        verbose_name ='streamx任务表'
        verbose_name_plural = 'streamx任务表'
