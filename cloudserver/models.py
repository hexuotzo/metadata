from django.db import models

# Create your models here.


class CloudServerDepartment(models.Model):
    id = models.IntegerField(primary_key=True)
    depart_name = models.CharField(max_length=100, blank=True, null=True)
    depart_level = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.depart_name

    def __str__(self):
        return u"%s" % self.depart_name

    class Meta:
        managed = False
        db_table = 'cloud_server_department'

class CloudServerPhysicalMachine(models.Model):
    device_id = models.CharField("设备ID", max_length=255, blank=True, null=True)
    host_name = models.CharField("主机名", max_length=255, blank=True, null=True)
    serial_number = models.CharField("序列号", max_length=255, blank=True, null=True)
    cabinet = models.CharField("机柜", max_length=255, blank=True, null=True)
    cabinet_position_start = models.IntegerField("起始U位", blank=True, null=True)
    cabinet_position_end = models.IntegerField("结束U位", blank=True, null=True)
    manage_ip = models.CharField("管理IP", max_length=100, blank=True, null=True)
    machine_room = models.CharField("机房", max_length=100, blank=True, null=True)
    server_factory_date = models.CharField("服务器出厂日期", max_length=100, blank=True, null=True)
    cpu_cores_num = models.IntegerField("CPU 核", blank=True, null=True)
    cpu_model = models.CharField("CPU型号", max_length=100, blank=True, null=True)
    memory_size = models.IntegerField("内存 GB", blank=True, null=True)
    gpu_num = models.IntegerField("GPU数量", blank=True, null=True)
    gpu_conf = models.CharField("GPU配置", max_length=255, blank=True, null=True)
    disk_num = models.IntegerField("磁盘数量", blank=True, null=True)
    disk_conf = models.CharField("磁盘配置", max_length=255, blank=True, null=True)
    calculation_node_type = models.CharField("计算节点类型", max_length=255, blank=True, null=True)
    system = models.CharField("操作系统", max_length=100, blank=True, null=True)
    system_version = models.CharField("操作系统版本", max_length=100, blank=True, null=True)
    network_environment = models.CharField("网络环境", max_length=100, blank=True, null=True)
    usage_scenario = models.CharField("使用场景", max_length=100, blank=True, null=True)
    ip_adress = models.CharField("IP地址", max_length=100, blank=True, null=True)
    storage = models.CharField("存储空间", max_length=100, blank=True, null=True)
    load = models.CharField("负载", max_length=100, blank=True, null=True)
    application_program = models.CharField("应用程序", max_length=100, blank=True, null=True)
    project = models.CharField("所属项目", max_length=100, blank=True, null=True)
    model = models.CharField("模块", max_length=100, blank=True, null=True)
    functionality = models.CharField("应用功能说明", max_length=100, blank=True, null=True)
    first_level_department = models.ForeignKey(CloudServerDepartment,limit_choices_to={"depart_level":1},to_field="id",related_name="first_level_department_name",db_column="first_level_department",verbose_name='一级部门',blank=True, null=True, on_delete=models.CASCADE)
    secondary_level_department = models.ForeignKey(CloudServerDepartment,limit_choices_to={"depart_level":2}, to_field="id",related_name="secondary_level_department_name",db_column="secondary_level_department", verbose_name='二级部门',blank=True, null=True, on_delete=models.CASCADE)
    third_level_department = models.ForeignKey(CloudServerDepartment,limit_choices_to={"depart_level":3}, to_field="id",related_name="third_level_department_name", db_column="third_level_department" ,blank=True, verbose_name='三级部门',null=True, on_delete=models.CASCADE)
    user = models.CharField("使用人", max_length=100, blank=True, null=True)
    confirm_in_use = models.CharField("确认在用", max_length=100, blank=True, null=True)
    notes = models.CharField("备注", max_length=255, blank=True, null=True)
    asset_ownership = models.CharField("资产归属", max_length=100, blank=True, null=True)
    initial_valuation_of_assets = models.CharField("资产初始估值", max_length=255, blank=True, null=True)
    service = models.CharField("服务商", max_length=100, blank=True, null=True)
    corresponding_contract = models.CharField("对应合同", max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cloud_server_physical_machine'
        verbose_name = "物理机"
        verbose_name_plural = "物理机"