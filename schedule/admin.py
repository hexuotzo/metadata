from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime
import json
from schedule.models import (Project,ProjectUser,Task,TaskDepend,TaskLog,MonitorOff,MonitorReceiver,MonitorReal,StreamxTask)
from django.forms.models import model_to_dict
from django.http import HttpResponse,HttpResponseRedirect

class ScheduleProjectAdmin(admin.ModelAdmin):
    list_display = [ 'id','project_name','user_name','create_time','update_time','update_user_name','edit_action']
    #search_fields = ['project_name']

    list_per_page = 20
    add_form_template = 'admin/metadata/project_add.html'
    change_form_template = 'admin/metadata/project_edit.html'

    list_display_links = None

    def edit_action(self, obj):
        uri = "/admin/schedule/project/%s/change" % (obj.id)
        return mark_safe('<a href="%s">修改</a>' % (uri))

    edit_action.short_description = '操作'

    def add_view(self, request, form_url='', extra_context={}):
        userList = User.objects.all()
        extra_context['user_list'] = userList

        if request.POST:
            postData = request.POST
            current_user = request.user

            # 项目名称重复验证
            insertDict = {
                'project_name' : postData['project_name'],
                'project_desc' : postData['project_desc'],
                'user_name' : current_user.username,
                'update_user_name' : current_user.username,
                'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            project = Project.objects.create(**insertDict)
            if project.id > 0:
                owner = postData.getlist('owner[]')
                for userId  in owner:
                    ownerDict = {
                        'project_id' : project.id,
                        'user_id' : userId
                    }
                    # 插入数据
                    ProjectUser.objects.create(**ownerDict)

            #return HttpResponse(project.id)

            return HttpResponseRedirect("/admin/schedule/project")


        return super(ScheduleProjectAdmin,self).add_view(request,extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': True,
                         'readonly': True}
        extra_context['object_id'] = object_id
        project_info = Project.objects.get(pk=object_id)

        userList = User.objects.all()

        proOwner =  ProjectUser.objects.filter(project_id=object_id)
        projectUserList = []
        for project in proOwner:
            projectUserList.append(project.user_id)

        extra_context['user_list'] = userList
        extra_context['project'] = project_info
        extra_context['project_user_list'] = projectUserList


        if request.POST:
            postData = request.POST
            current_user = request.user

            objectQ = Project.objects.get(pk=postData['id'])

            objectQ.project_name = postData['project_name']
            objectQ.project_desc = postData['project_desc']
            objectQ.update_user_name = current_user.username
            objectQ.save()

            owner = postData.getlist('owner[]')

            # 将接收的user_id和表里面已经存在的user_id做对比，分这种情况
            # 1.接收的user_id在表面不存在则插入
            # 2.表里面的id在接收里面不存在，需要做删除
            postId = []
            projectUserId = []
            for userId in owner:
                postId.append(userId)

            projectUserObject = ProjectUser.objects.filter(project_id=postData['id'])
            for project in projectUserObject:
                projectUserId.append(project.user_id)

            addStr =''
            for i in postId:
                if int(i) in projectUserId:
                    pass
                else:
                    insertDict = {
                        'project_id' : postData['id'],
                        'user_id' : i
                    }
                    addStr += str(i) + ','
                    ProjectUser.objects.create(**insertDict)
            # 8,add [2,3,4,7]
            deleteStr = ''
            for i in projectUserId:
                if str(i) in postId:
                    pass
                else:
                    #pass
                    ProjectUser.objects.filter(project_id=postData['id'],user_id=i).delete()
                    deleteStr += str(i)+','
            #return HttpResponse("add:%s,delete:%s"%(addStr,deleteStr))

            return HttpResponseRedirect("/admin/schedule/project")

        return super(ScheduleProjectAdmin, self).change_view(request, object_id, extra_context=extra_context)

admin.site.register(Project, ScheduleProjectAdmin)


# 任务列表
class ScheduleTaskAdmin(admin.ModelAdmin):
    list_display = [ 'id','task_name','task_type','owner_name', 'project_id','task_identification','frequency','status', 'create_time','update_time','edit_action']
    search_fields = ['task_identification','task_name']
    list_filter = ['project_id', 'task_type']

    list_per_page = 20
    add_form_template = 'admin/metadata/task_add.html'
    change_form_template = 'admin/metadata/task_edit.html'

    list_display_links = None

    def edit_action(self, obj):
        uri = "/admin/schedule/task/%s/change" % (obj.id)
        return mark_safe('<a href="%s">修改</a>' % (uri))

    edit_action.short_description = '操作'

    def add_view(self, request, form_url='', extra_context={}):
        userList = User.objects.all()
        extra_context['user_list'] = userList

        projectList = Project.objects.all()
        sql = '''
            select t.task_identification,t.id,t.project_id,p.project_name
            from schedule_task t
            left join schedule_project p on t.project_id=p.id
            where t.status=1
        '''
        taskTag = Task.objects.raw(sql)
        extra_context['project_list'] = projectList
        extra_context['task_tag'] = taskTag

        if request.POST:
            postData = request.POST
            current_user = request.user
            project_id = Project.objects.get(id=postData['project_id'])
            insertDict = {
                'project_id' : project_id,
                'task_identification' : postData['task_identification'],
                'task_name' : postData['task_name'],
                'task_desc' : postData['task_desc'],
                'owner_name' : postData['owner_name'],
                'frequency' : postData['frequency'],
                'execute_command' : postData['execute_command'],
                'task_type' : 1,
                'user_id' : current_user.id,
                'update_user_id' : current_user.id,
                'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'update_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status' : postData['status'],
                'import_type' : 0,
            }
            taskObj = Task.objects.create(**insertDict)

            # 插入依赖关系task_depend
            dependList = postData.getlist('task_depend[]')
            if taskObj:
                for dependId in dependList:
                    dependDict = {
                        'task_id' : taskObj.id,
                        'parent_task_id' : dependId,
                        'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    TaskDepend.objects.create(**dependDict)

            return HttpResponseRedirect("/admin/schedule/task")


        return super(ScheduleTaskAdmin,self).add_view(request,extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': True,
                         'readonly': True}
        extra_context['object_id'] = object_id

        sql = '''
            select t.task_identification,t.id,t.project_id,p.project_name
            from schedule_task t
            left join schedule_project p on t.project_id=p.id
            where t.status=1
        '''
        taskTag = Task.objects.raw(sql)

        taskInfo = Task.objects.get(pk=object_id)
        projectList = Project.objects.all()

        dependAll =  TaskDepend.objects.filter(task_id=object_id)
        dependAllList = []
        for depend in dependAll:
            dependAllList.append(depend.parent_task_id)

        userList = User.objects.all()
        extra_context['user_list'] = userList

        #return HttpResponse(taskInfo.project_id.id)
        extra_context['project_list'] = projectList
        extra_context['task_info'] = taskInfo
        extra_context['task_tag'] = taskTag
        extra_context['depend_all'] = dependAllList


        if request.POST:
            postData = request.POST
            current_user = request.user

            beforeDict = model_to_dict(Task.objects.get(pk=postData['id']))

            objectQ = Task.objects.get(pk=postData['id'])
            project_id = Project.objects.get(id=postData['project_id'])

            objectQ.project_id = project_id
            objectQ.task_name = postData['task_name']
            objectQ.task_desc = postData['task_desc']
            objectQ.owner_name = postData['owner_name']
            objectQ.frequency = postData['frequency']
            objectQ.execute_command = postData['execute_command']
            objectQ.status = postData['status']
            objectQ.update_user_id = current_user.id
            objectQ.save()

            #依赖关系修改
            TaskDepend.objects.filter(task_id=postData['id']).delete()

            dependList = postData.getlist('task_depend[]')

            for dependId in dependList:
                dependDict = {
                    'task_id': postData['id'],
                    'parent_task_id': dependId,
                    'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                TaskDepend.objects.create(**dependDict)

            #记录日志
            afterDict = model_to_dict(Task.objects.get(pk=postData['id']))

            logDict = {
                'task_id' : postData['id'],
                'edit_before':json.dumps(beforeDict),
                'edit_before_user' : User.objects.get(pk=beforeDict['user_id']).username,
                'edit_after' : json.dumps(afterDict),
                'edit_after_user' : current_user.username,
                'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            TaskLog.objects.create(**logDict)

            return HttpResponseRedirect("/admin/schedule/task")

        return super(ScheduleTaskAdmin, self).change_view(request, object_id, extra_context=extra_context)

admin.site.register(Task, ScheduleTaskAdmin)


# 任务列表
class MonitorOffAdmin(admin.ModelAdmin):
    list_display = [ 'id','monitor_name','monitor_type','owner_name', 'monitor_mode','status','create_time','update_time','edit_action']
    search_fields = ['task_identification','monitor_name']
    list_filter = ['monitor_name', 'monitor_type','task_identification']

    list_per_page = 20
    add_form_template = 'admin/metadata/monitor_off_add.html'
    change_form_template = 'admin/metadata/monitor_off_edit.html'

    list_display_links = None

    class Media:
        js = ["/static/js/monitor.js"]

    def edit_action(self, obj):
        if obj.monitor_mode in (1,2):
            uri = "/admin/schedule/monitoroff/%s/change" % (obj.id)
        else:
            uri = "/admin/schedule/monitorreal/%s/change" % (obj.id)
        return mark_safe('<a href="%s">修改</a>' % (uri))

    edit_action.short_description = '操作'

    def add_view(self, request, form_url='', extra_context={}):
        #获取任务标识
        taskAll = Task.objects.filter(project_id=1)
        extra_context['task_all'] = taskAll

        #责任人
        userList = User.objects.all()
        extra_context['user_list'] = userList

        #获取报警接收人及项目
        projectAll = Project.objects.all()
        extra_context['project_list'] = projectAll

        projectAndUser = []
        for project in projectAll:
            projectDict = {}
            projectDict['id'] = '1-' +str(project.id)
            projectDict['name'] = '项目-' + project.project_name
            projectAndUser.append(projectDict)

        for user in userList:
            userDict = {}
            userDict['id'] = '2-' + str(user.id)
            userDict['name'] = '用户-' + user.username
            projectAndUser.append(userDict)

        extra_context['project_and_user'] = projectAndUser


        #finish time list
        finish_time = range(8,17)
        extra_context['finish_time'] = finish_time

        run_time = range(1,6)
        extra_context['run_time'] = run_time

        if request.POST:
            postData = request.POST
            current_user = request.user
            #print(postData)
            insertDict = {
                'monitor_type' : 1,
                'task_identification' : postData['task_identification'],
                'monitor_name' : postData['monitor_name'],
                'owner_name' : postData['owner_id'],
                'monitor_mode': postData['monitor_mode'],
                'finish_time': postData['finish_time'] if postData['monitor_mode']=='1' else 0,
                'run_time' : postData['run_time'] if postData['monitor_mode']=='2' else 0,
                'status' : postData['status'],
                'monitor_value' : '0',
                'is_warning_custom' : postData['is_warning_custom'],
                'warning_send_time' : postData['warning_send_time'],
                'warning_type' : postData['warning_type'],
                'user_id' : current_user.id,
                'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            monitorObj = MonitorOff.objects.create(**insertDict)

            # 插入接收人信息
            receiveList = postData.getlist('receivers[]')
            for receive in receiveList:
                receiveType = receive.split('-')
                insertDict = {
                    'monitor_id' : monitorObj.id,
                    'user_type' : receiveType[0],
                    'user_id' : receiveType[1],
                    'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                MonitorReceiver.objects.create(** insertDict)

            return HttpResponseRedirect("/admin/schedule/monitoroff")


        return super(MonitorOffAdmin,self).add_view(request,extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': True,
                         'readonly': True}
        extra_context['object_id'] = object_id

        # 获取任务标识
        taskAll = Task.objects.filter(project_id=1)
        extra_context['task_all'] = taskAll

        # 责任人
        userList = User.objects.all()
        extra_context['user_list'] = userList

        # 获取报警接收人及项目
        projectAll = Project.objects.all()
        extra_context['project_list'] = projectAll

        projectAndUser = []
        for project in projectAll:
            projectDict = {}
            projectDict['id'] = '1-' +str(project.id)
            projectDict['name'] = '项目-' + project.project_name
            projectAndUser.append(projectDict)

        for user in userList:
            userDict = {}
            userDict['id'] = '2-' + str(user.id)
            userDict['name'] = '用户-' + user.username
            projectAndUser.append(userDict)

        extra_context['project_and_user'] = projectAndUser

        # 获取已经设置的接收人
        receiverAll = MonitorReceiver.objects.filter(monitor_id=object_id)
        receiver = []
        for rece in receiverAll:
            receStr = str(rece.user_type) +'-'+ str(rece.user_id)
            receiver.append(receStr)

        extra_context['receiver'] = receiver


        taskMonitor = MonitorOff.objects.get(pk=object_id)
        taskMonitor.finish_time = int(taskMonitor.finish_time)
        taskMonitor.run_time = int(taskMonitor.run_time)
        extra_context['task_monitor'] = taskMonitor

        #finish time list
        finish_time = range(8,17)
        extra_context['finish_time'] = finish_time

        run_time = range(1,6)
        extra_context['run_time'] = run_time


        if request.POST:
            postData = request.POST
            current_user = request.user
            monitor_q = MonitorOff.objects.get(pk=postData['id'])
            monitor_q.task_identification = postData['task_identification']
            monitor_q.monitor_name = postData['monitor_name']
            monitor_q.owner_name = postData['owner_id']
            monitor_q.monitor_mode = postData['monitor_mode']
            monitor_q.status = postData['status']
            monitor_q.finish_time = postData['finish_time'] if postData['monitor_mode']=='1' else 0
            monitor_q.run_time = postData['run_time'] if postData['monitor_mode']=='2' else 0
            monitor_q.is_warning_custom = postData['is_warning_custom']
            monitor_q.warning_send_time = postData['warning_send_time']
            monitor_q.warning_type = postData['warning_type']
            monitor_q.save()

            MonitorReceiver.objects.filter(monitor_id=postData['id']).delete()

            # 插入接收人信息
            receiveList = postData.getlist('receivers[]')
            for receive in receiveList:
                receiveType = receive.split('-')
                insertDict = {
                    'monitor_id': postData['id'],
                    'user_type': receiveType[0],
                    'user_id': receiveType[1],
                    'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                MonitorReceiver.objects.create(**insertDict)


            return HttpResponseRedirect("/admin/schedule/monitoroff")

        return super(MonitorOffAdmin, self).change_view(request, object_id, extra_context=extra_context)

admin.site.register(MonitorOff, MonitorOffAdmin)


# 实时监控
class MonitorRealtimeAdmin(admin.ModelAdmin):
    add_form_template = 'admin/metadata/monitor_realtime_add.html'
    change_form_template = 'admin/metadata/monitor_realtime_edit.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        thirtyday = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')


        #extra_content['unit'] = storageUnit

        return super(MonitorRealtimeAdmin, self).change_view(request, object_id, extra_context=extra_content)

    def add_view(self, request, form_url='', extra_context={}):
        #获取任务标识
        taskAll = StreamxTask.objects.all()
        extra_context['task_all'] = taskAll

        #责任人
        userList = User.objects.all()
        #print(userList)
        extra_context['user_list'] = userList

        #获取报警接收人及项目
        projectAll = Project.objects.all()
        extra_context['project_list'] = projectAll

        projectAndUser = []
        for project in projectAll:
            projectDict = {}
            projectDict['id'] = '1-' +str(project.id)
            projectDict['name'] = '项目-' + project.project_name
            projectAndUser.append(projectDict)

        for user in userList:
            userDict = {}
            userDict['id'] = '2-' + str(user.id)
            userDict['name'] = '用户-' + user.username
            projectAndUser.append(userDict)

        extra_context['project_and_user'] = projectAndUser

        if request.POST:
            postData = request.POST
            current_user = request.user
            #print(postData)

            task_identification = postData['task_identification']
            kafka_dict = {}
            if postData['monitor_mode'] == '3':
                kafka_dict = {
                    'brokes' : postData['brokes'],
                    'topic' : postData['topic'],
                    'group_id' : postData['group_id'],
                    'max_value' : postData['max_value'],
                }
            elif postData['monitor_mode'] == '4':

                if postData['task_from'] == '2':
                    kafka_dict = {
                        'ip': postData['task_ip'],
                        'task_name_custom' : postData['task_name_custom'],
                    }
                    task_identification = postData['task_name_custom']
            else:
                kafka_dict = {}


            insertDict = {
                'monitor_type' : 2,
                'task_identification' : task_identification,
                'monitor_name' : postData['monitor_name'],
                'owner_name' : postData['owner_id'],
                'monitor_mode': postData['monitor_mode'],
                'task_from' : postData['task_from'],
                'finish_time':  0,
                'run_time' :  0,
                'status': postData['status'],
                'monitor_value' : json.dumps(kafka_dict),
                'is_warning_custom' : postData['is_warning_custom'],
                'warning_send_time' : postData['warning_send_time'],
                'warning_type' : postData['warning_type'],
                'user_id' : current_user.id,
                'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            monitorObj = MonitorOff.objects.create(**insertDict)

            # 插入接收人信息
            receiveList = postData.getlist('receivers[]')
            for receive in receiveList:
                receiveType = receive.split('-')
                insertDict = {
                    'monitor_id' : monitorObj.id,
                    'user_type' : receiveType[0],
                    'user_id' : receiveType[1],
                    'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                MonitorReceiver.objects.create(** insertDict)

            return HttpResponseRedirect("/admin/schedule/monitoroff")

        return super(MonitorRealtimeAdmin,self).add_view(request,extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': True,
                         'readonly': True}
        extra_context['object_id'] = object_id

        taskAll = StreamxTask.objects.all()
        extra_context['task_all'] = taskAll

        # 责任人
        userList = User.objects.all()
        extra_context['user_list'] = userList

        # 获取报警接收人及项目
        projectAll = Project.objects.all()
        extra_context['project_list'] = projectAll

        projectAndUser = []
        for project in projectAll:
            projectDict = {}
            projectDict['id'] = '1-' +str(project.id)
            projectDict['name'] = '项目-' + project.project_name
            projectAndUser.append(projectDict)

        for user in userList:
            userDict = {}
            userDict['id'] = '2-' + str(user.id)
            userDict['name'] = '用户-' + user.username
            projectAndUser.append(userDict)

        extra_context['project_and_user'] = projectAndUser

        # 获取已经设置的接收人
        receiverAll = MonitorReceiver.objects.filter(monitor_id=object_id)
        receiver = []
        for rece in receiverAll:
            receStr = str(rece.user_type) +'-'+ str(rece.user_id)
            receiver.append(receStr)

        extra_context['receiver'] = receiver

        taskMonitor = MonitorOff.objects.get(pk=object_id)

        monitor_dict = json.loads(taskMonitor.monitor_value)
        extra_context['task_monitor'] = taskMonitor
        extra_context['monitor_dict'] = monitor_dict
        print(monitor_dict)
        if request.POST:
            postData = request.POST
            current_user = request.user

            task_identification = postData['task_identification']
            kafka_dict = {}
            if postData['monitor_mode'] == '3':
                kafka_dict = {
                    'brokes': postData['brokes'],
                    'topic': postData['topic'],
                    'group_id': postData['group_id'],
                    'max_value': postData['max_value'],
                }
            elif postData['monitor_mode'] == '4':

                if postData['task_from'] == '2':
                    kafka_dict = {
                        'ip': postData['task_ip'],
                        'task_name_custom': postData['task_name_custom'],
                    }
                    task_identification = postData['task_name_custom']
                else:
                    kafka_dict = {}
            else:
                kafka_dict = {}

            monitor_q = MonitorOff.objects.get(pk=postData['id'])
            monitor_q.task_identification = task_identification
            monitor_q.monitor_name = postData['monitor_name']
            monitor_q.owner_name = postData['owner_id']
            monitor_q.monitor_mode = postData['monitor_mode']
            monitor_q.task_from = postData['task_from'] if postData['task_from'] in ('1','2') else 0
            monitor_q.monitor_value = json.dumps(kafka_dict)
            monitor_q.status = postData['status']
            monitor_q.finish_time = 0
            monitor_q.run_time = 0
            monitor_q.is_warning_custom = postData['is_warning_custom']
            monitor_q.warning_send_time = postData['warning_send_time']
            monitor_q.warning_type = postData['warning_type']
            monitor_q.save()

            MonitorReceiver.objects.filter(monitor_id=postData['id']).delete()

            # 插入接收人信息
            receiveList = postData.getlist('receivers[]')
            for receive in receiveList:
                receiveType = receive.split('-')
                insertDict = {
                    'monitor_id': postData['id'],
                    'user_type': receiveType[0],
                    'user_id': receiveType[1],
                    'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                MonitorReceiver.objects.create(**insertDict)


            return HttpResponseRedirect("/admin/schedule/monitoroff")

        return super(MonitorRealtimeAdmin, self).change_view(request, object_id, extra_context=extra_context)

admin.site.register(MonitorReal, MonitorRealtimeAdmin)