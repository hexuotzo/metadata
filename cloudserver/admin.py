from django.contrib import admin
from cloudserver.models import *


# Register your models here.
@admin.register(CloudServerPhysicalMachine)
class CloudServerPhysicalMachineAdmin(admin.ModelAdmin):
    search_fields = ("device_id", "host_name", "cabinet", "manage_ip", "ip_adress", "first_level_department__depart_name",
                     "secondary_level_department__depart_name", "third_level_department__depart_name", "user")
    list_filter = (
        "cabinet", "system", "first_level_department", "secondary_level_department", "third_level_department")
    list_display = (
    "device_id", "serial_number", "cabinet", "machine_room", "server_factory_date", "cpu_cores_num", "memory_size",
    "system", "network_environment", "usage_scenario", "ip_adress", "get_first_level_department",
    "get_secondary_level_department", "get_third_level_department", "user", "confirm_in_use", "asset_ownership")


    def get_first_level_department(self, obj):
        return obj.first_level_department.depart_name if obj.first_level_department else ""
    get_first_level_department.short_description = "一级部门"

    def get_secondary_level_department(self, obj):
        return obj.secondary_level_department.depart_name if obj.secondary_level_department else ""
    get_secondary_level_department.short_description = "二级部门"

    def get_third_level_department(self, obj):
        return obj.third_level_department.depart_name if obj.third_level_department else ""
    get_third_level_department.short_description = "三级部门"