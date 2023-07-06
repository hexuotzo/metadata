from django.urls import re_path as url
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static

from metadata.views import search_basic_column_info,pcc_vehicle_export_excel,pcc_upgrade_export_excel,pcc_problem_export_excel,pcc_depot_export_excel,column_list,column_edit,table_dependency,t_search,t_detail,get_table_name,get_column_name,rule_execute_now
# from schedule.views import get_is_exist_task_name,get_is_exist_project_name,get_zip_test,get_monitor_exist
from usertags import views as usertag_views

urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')), 
    url(r'^admin/', admin.site.urls),

    # url(r'^ajax/search_basic_column_info/', search_basic_column_info),
    # url(r'^ajax/pcc_vehicle_export_excel/', pcc_vehicle_export_excel),
    # url(r'^ajax/pcc_upgrade_export_excel/', pcc_upgrade_export_excel),
    # url(r'^ajax/pcc_problem_export_excel/', pcc_problem_export_excel),
    # url(r'^ajax/pcc_depot_export_excel/', pcc_depot_export_excel),
    # url(r'^column/column_list/', column_list),
    url(r'^column/column_edit/', column_edit),
    # url(r'^hive/reply/', table_dependency),
    # url(r'^hive/search/*', t_search),
    # url(r'^ajax/get_table_name/*', get_table_name),
    # url(r'^ajax/get_column_name/*', get_column_name),
    # url(r'^ajax/rule_execute_now/*', rule_execute_now),
    # url(r'^ajax/get_task_exist/*', get_is_exist_task_name),
    # url(r'^ajax/get_project_exist/*', get_is_exist_project_name),
    # url(r'^ajax/get_zip_test/*', get_zip_test),
    # url(r'^ajax/get_monitor_exist/*', get_monitor_exist),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
