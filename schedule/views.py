from django.shortcuts import render

# Create your views here.
from schedule.models import Project,Task,MonitorOff
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from schedule.flow_auto_upload import flow_generate_and_upload

# ajax验证是否存在相同的项目和任务标识
def get_is_exist_task_name(request):
    project_id = request.GET['project_id']
    identification_name = request.GET['task_identification']
    taskInfo = Task.objects.filter(project_id=project_id,task_identification=identification_name)

    if taskInfo:
        return JsonResponse({
            'success': 'error'
        })
    else:
        return JsonResponse({
            'success':'ok'
        })

# ajax验证是否存在相同的项目名称
def get_is_exist_project_name(request):
    project_name = request.GET['project_name']
    projectInfo = Project.objects.filter(project_name=project_name)

    if projectInfo:
        return JsonResponse({
            'success': 'error'
        })
    else:
        return JsonResponse({
            'success':'ok'
        })

# ajax验证是否存在相同的项目名称
def get_monitor_exist(request):
    monitor_mode = request.GET['monitor_mode']
    task_identification = request.GET['task_identification']

    monitor_info = MonitorOff.objects.filter(task_identification=task_identification,monitor_mode=monitor_mode,monitor_type=1)

    if monitor_info:
        return JsonResponse({
            'success': 'error'
        })
    else:
        return JsonResponse({
            'success':'ok'
        })

# 打包测试接口
def get_zip_test(request):
    task_identification = request.GET['job_name']
    project_id = request.GET['project_id']
    frequency = request.GET['frequency']
    execute_command = request.GET['execute_command']
    depend = request.GET['depend']
    print(execute_command)
    print('---------')
    print(execute_command.replace("\r\n", "@"))

    flowReturn = flow_generate_and_upload(project_id,task_identification,frequency,execute_command,depend)
    print(flowReturn)


    return JsonResponse(flowReturn)




