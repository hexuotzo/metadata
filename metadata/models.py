# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cgi
import re


from django.db import models

class QingQiJieFangAppAction(models.Model):
    action = models.CharField('行为事件', max_length=100, primary_key=True)

    class Meta:
        verbose_name = '青汽解放行APP_行为事件'
        verbose_name_plural = "青汽解放行APP_行为事件信息管理"
        managed = False

    def __unicode__(self):
        return "%s" % self.action


class QingQiJieFangAppMod(models.Model):
    modid = models.CharField('模块ID', max_length=100, primary_key=True)
    modname = models.CharField('模块名', max_length=100)

    class Meta:
        verbose_name = '青汽解放行APP_模块'
        verbose_name_plural = "青汽解放行APP_模块管理"
        managed = False

    def __unicode__(self):
        return "%s %s" % (self.modid, self.modname)


class AppBuriedPoint(models.Model):
    modid = models.CharField('模块编码', max_length=40)
    modname = models.CharField('模块名称', max_length=20)
    action = models.CharField('行为', max_length=20)
    pageid = models.CharField('页面编码', max_length=40)
    pagename = models.CharField('页面名称', max_length=20)
    appid = models.CharField('所属APP编码', max_length=40)	
    appname = models.CharField('所属APP名称', max_length=20)	
    labelid = models.CharField('标签编码', max_length=40)
    lablename = models.CharField('标签名', max_length=40)

    class Meta:
        verbose_name = 'APP埋点'
        verbose_name_plural = "APP埋点管理"
        unique_together = (("appid", "pageid", "labelid"),)

    def __unicode__(self):
        return "%s %s" % (self.labelid, self.lablename)



class MonitorMakefileTag(models.Model):
    tagchn = models.CharField('标记中文名称', db_column='tagChn', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tageng = models.CharField('标记英文名称', db_column='tagEng', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    finishtime = models.CharField('预期生成时间点', db_column='finishTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycle = models.CharField('生命周期', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor_makefile_tag'
        verbose_name = 'MAKEFILE标记'
        verbose_name_plural = "MAKEFILE标记管理"


class MdTableInfoRecord(models.Model):
    source = models.CharField('数据源', max_length=20, blank=True, null=True)
    database_name = models.CharField('数据库', max_length=100, blank=True, null=True)
    table_eng = models.CharField('表英文名称', max_length=100, blank=True, null=True)
    table_chi = models.CharField('表中文名称', max_length=100, blank=True, null=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, auto_now_add=False)
    show_tag = models.IntegerField('发送标记', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md_table_info_record'
        unique_together = (('source', 'database_name', 'table_eng'),)
        verbose_name = '集群表基本信息'
        verbose_name_plural = "集群表基本信息管理"


class RelMdTableTable(models.Model):
    """
    指标层级关系, 父子ID都使用md_index_info表. 多对多关联
    """
    p_table_id = models.ForeignKey('MdIndexInfo', db_column='p_table_id', verbose_name='源指标', on_delete=models.CASCADE)
    c_table_id = models.ForeignKey('MdIndexInfo', related_name="c_table_id", db_column='c_table_id', verbose_name='父指标', on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = '指标信息关系'
        verbose_name_plural = "指标信息关系"
        db_table = 'rel_md_table_table'
        unique_together = (("p_table_id", "c_table_id"),)
        

class MdIndexInfo(models.Model):
    index_name = models.CharField('指标英文名称', max_length=50, unique=True)
    index_desc = models.CharField('指标中文名称', max_length=100, blank=True, null=True)
    source_table = models.CharField('所在表', max_length=100, blank=True, null=True)
    index_unit = models.CharField('指标计量单位', max_length=20, blank=True, null=True)
    data_type = models.CharField('指标数据类型', max_length=20, blank=True, null=True)
    index_definition = models.CharField('指标定义', max_length=100, blank=True, null=True)
    index_rule = models.TextField('规则详述', blank=True, null=True)
    # parent_index = models.ManyToManyField('MdIndexInfo', 
    #     through='RelMdTableTable', 
    #     symmetrical=False,
    #     through_fields=('p_table_id', 'c_table_id'),
    #     verbose_name='父指标m2m',
    #     blank=True,
    #     default=None)
    index_owner = models.CharField('指标负责人', max_length=100, blank=True, null=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, auto_now_add=False, blank=True, null=True)
    update_editor = models.CharField('最新修改人', max_length=100, blank=True, null=True)
    create_editor = models.CharField('创建人', max_length=100, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'md_index_info'
        verbose_name = '指标信息'
        verbose_name_plural = "指标信息管理"
    
    def __unicode__(self):
        return "%s: %s(%s)" % (self.pk, self.index_desc, self.index_name)


class MdIndexInfoLog(models.Model):
    index_name = models.CharField('指标英文名称', max_length=50)
    index_desc = models.CharField('指标中文名称', max_length=100, blank=True, null=True)
    source_table = models.CharField('数据来源', max_length=100, blank=True, null=True)
    index_unit = models.CharField('指标计量单位', max_length=20, blank=True, null=True)
    data_type = models.CharField('指标数据类型', max_length=20, blank=True, null=True)
    index_definition = models.CharField('指标定义', max_length=100, blank=True, null=True)
    index_rule = models.TextField('规则详述', blank=True, null=True)
    parent_index = models.CharField('父指标', max_length=255, blank=True, null=True)
    index_owner = models.CharField('指标负责人', max_length=100, blank=True, null=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, auto_now_add=False, blank=True, null=True)
    update_editor = models.CharField('最新修改人', max_length=100, blank=True, null=True)
 
    class Meta:
        db_table = 'md_index_info_log'
        verbose_name = '指标信息修改记录'
        verbose_name_plural = "指标信息修改记录"

    def __unicode__(self):
        return "%s %s" % (self.index_desc, self.index_name)


class FieldInfo0020(models.Model):
    file_protoc = models.CharField('字段协议', max_length=11)
    field_name_en = models.CharField('字段英文名称', max_length=50)
    field_name_ch = models.CharField('字段中文名称', max_length=50, blank=True, null=True)
    field_unit = models.CharField('单位', max_length=50, blank=True, null=True)
    field_type = models.CharField('字段类型', max_length=50, blank=True, null=True)
    # field_min = models.CharField('字段阈值MIN', max_length=50, blank=True, null=True)
    # field_max = models.CharField('字段阈值MAX', max_length=50, blank=True, null=True)
    threshold = models.CharField('阈值(sql过滤条件)', max_length=255, blank=True, null=True)
    threshold_zh = models.CharField('阈值中文解释', max_length=255, blank=True, null=True)
    is_monitor = models.IntegerField('是否监控', choices=((1,'正在监控'),(-1,'未监控')), default=-1)
    field_explain = models.CharField('字段释义', max_length=50, blank=True, null=True)
    available = models.CharField('调研记录', max_length=255, blank=True, null=True, default='')
    field_orig = models.CharField('字段来源', max_length=50)
    operator = models.CharField('编辑人', max_length=50, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)
    edit_time = models.DateTimeField('编辑时间', auto_now=True, auto_now_add=False, blank=True, null=True)

    class Meta:
        db_table = '0200_field_info'
        verbose_name = '基础字段信息'
        verbose_name_plural = "基础字段信息管理"
        unique_together = (("field_name_en", "field_orig"),)

    def __unicode__(self):
        return "%s %s" % (self.field_name_ch, self.field_name_en)


class FieldInfo0020Log(models.Model):
    file_protoc = models.CharField('字段协议', max_length=11)
    field_name_en = models.CharField('字段英文名称', max_length=50, blank=True, null=True)
    field_name_ch = models.CharField('字段中文名称', max_length=50, blank=True, null=True)
    field_unit = models.CharField('单位', max_length=50, blank=True, null=True)
    field_type = models.CharField('字段类型', max_length=50, blank=True, null=True)
    # field_min = models.CharField('字段阈值MIN', max_length=50, blank=True, null=True)
    # field_max = models.CharField('字段阈值MAX', max_length=50, blank=True, null=True)
    threshold = models.CharField('阈值(sql过滤条件)', max_length=255, blank=True, null=True)
    threshold_zh = models.CharField('阈值中文解释', max_length=255, blank=True, null=True)
    is_monitor = models.IntegerField('是否监控', choices=((1,'正在监控'),(-1,'未监控')), default=-1)
    field_explain = models.CharField('字段释义', max_length=50, blank=True, null=True)
    available = models.CharField('调研记录', max_length=255, blank=True, null=True, default='')
    field_orig = models.CharField('字段来源', max_length=50, blank=True, null=True)
    operator = models.CharField('编辑人', max_length=50, blank=True, null=True)
    create_time = models.DateTimeField('修改时间', auto_now=False, auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = '0200_field_info_log'
        verbose_name = '基础字段信息修改记录'
        verbose_name_plural = "基础字段信息修改记录"

    def __unicode__(self):
        return "%s %s" % (self.field_name_ch, self.field_name_en)


class MdColumnBasicInfo(models.Model):
    column_id = models.CharField('字段ID', max_length=100, primary_key=True)
    column_name = models.CharField('字段名', max_length=100)
    column_type = models.CharField('字段类型', max_length=100)
    table_name = models.CharField('库表名', max_length=100)
    online_status = models.CharField('状态', max_length=10)

    def format_tablecolumn(self):
        return "%s,%s.%s" % (cgi.escape(self.column_type), self.table_name, self.column_name)

    def __unicode__(self):
        return "%s.%s" % (self.table_name, self.column_name)

    class Meta:
        db_table = 'md_column_basic_info'
        managed = False

class MdIndexParent(models.Model):
    md_index = models.ForeignKey(MdIndexInfo, on_delete=models.CASCADE)
    parent = models.CharField('指标查询', max_length=1, choices=(('1', '请选择'),))
    index_name = models.CharField('父指标英文名称', max_length=50)
    source_table = models.CharField('所在表', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'md_index_parent'
        verbose_name = '父指标'
        unique_together = (("md_index", "index_name", "source_table"),)


class MdThreshold(models.Model):
    '''
    指标阈值管理
    '''

    name = models.CharField('指标名', max_length=50)
    column_name = models.CharField('字段名', max_length=50, unique=True)
    val_min = models.IntegerField('最小阈值', default=None, blank=True, null=True)
    val_max = models.IntegerField('最大阈值', default=None, blank=True, null=True)
    default_val = models.IntegerField('默认值', default=-99, help_text="默认值-99", blank=True)
    desc = models.TextField('说明', blank=True, null=True)

    class Meta:
        db_table = 'md_index_threshold'
        verbose_name = '指标阈值'
        verbose_name_plural = "指标阈值管理"


class MdTsktagInfo(models.Model):
    '''
    任务标记管理
    '''
    task_tag = models.CharField('任务标记', max_length=64)
    task_type = models.CharField('任务类型', max_length=32)
    task_name = models.CharField('任务名称', max_length=128)
    task_desc = models.TextField('任务描述')
    task_owner = models.CharField('任务负责人', max_length=32)
    task_runtime = models.CharField('任务运行时间', max_length=10)
    is_online = models.IntegerField('是否上线', choices=((1,'上线'),(0,'下线'),(-1,'待上线')))
    online_time = models.DateTimeField('上线时间')
    downline_time = models.DateTimeField('下线时间')
    update_editor = models.CharField('最近修改人', max_length=32)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'md_tasktag_info'
        verbose_name = '数据质量监控任务'
        verbose_name_plural = '数据质量监控任务管理'



class PccDepotName(models.Model):
    """
    pcc车厂管理
    """
    depot_name = models.CharField('车厂名称', max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.depot_name

    class Meta:
        managed = False
        db_table = 'pcc_depot_name'
        verbose_name = 'pcc车厂'
        verbose_name_plural = 'pcc车厂管理'


class PccProblemDetail(models.Model):
    """
    pcc问题明细表
    """
    device_type = models.IntegerField("问题设备", choices=((1, "pcc"), (2, "tbox")), blank=True, null=True)
    behind_vid = models.CharField("问题车辆后装vid", max_length=50, blank=True, null=True)
    front_vid = models.CharField("问题车辆前装vid", max_length=50, blank=True, null=True)
    chassis_number = models.CharField("问题车辆底盘号", max_length=50, blank=True, null=True)
    problem_describe = models.CharField("问题描述", max_length=255, blank=True, null=True)
    problem_solution = models.CharField("解决办法", max_length=255, blank=True, null=True)
    status = models.IntegerField("状态", choices=((1, "已解决"), (2, "进行中"), (3, "终止")), blank=True,
                                 null=True)
    other_remark = models.CharField("其他备注", max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pcc_problem_detail'
        verbose_name = 'pcc问题明细'
        verbose_name_plural = 'pcc问题明细管理'


class PccUpgradeDetail(models.Model):
    """
    pcc升级明细表
    """
    upgrade_device = models.IntegerField("升级设备", choices=((1, "pcc"), (2, "tbox")), blank=True,
                                         null=True)
    behind_vid = models.CharField("后装vid", max_length=50, blank=True, null=True)
    front_vid = models.CharField("前装vid", max_length=50, blank=True, null=True)
    chassis_number = models.CharField("底盘号", max_length=50, blank=True, null=True)
    upgrade_time = models.DateTimeField("升级时间", blank=True, null=True)
    upgrade_version = models.CharField("升级版本", max_length=50, blank=True, null=True)
    other_remark = models.CharField("其他备注", max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pcc_upgrade_detail'
        verbose_name = 'pcc升级明细'
        verbose_name_plural = 'pcc升级明细管理'


class PccVehicleInfo(models.Model):
    """
    pcc车辆信息表
    """
    depot = models.ForeignKey(PccDepotName, models.DO_NOTHING, db_column='depot', blank=True, null=True,verbose_name="车厂")
    device_type = models.IntegerField("设备类型", choices=((1,"一体机"),(2,"分体机")),blank=True, null=True)
    install_type = models.IntegerField("安装类型", choices=((1,"前装"),(2,"后装")), blank=True, null=True)
    car_number = models.CharField("车牌号", max_length=50, blank=True, null=True)
    engine_model = models.CharField("发动机型号", max_length=50, blank=True, null=True)
    trans_model = models.CharField("变速箱型号", db_column='trans model', max_length=50, blank=True,null=True)
    trans_type = models.IntegerField("变速箱类型", choices=((1,'手动挡'),(2,'自动挡')), blank=True,null=True)
    front_sim = models.CharField("前装sim卡号", max_length=50, blank=True, null=True)
    behind_sim = models.CharField("后装sim卡号", max_length=50, blank=True, null=True)
    front_vid = models.CharField("前装vid", max_length=50, blank=True, null=True)
    behind_vid = models.CharField("后装vid", max_length=50)
    at_sn = models.CharField("AdasisTbox-SN", max_length=50,blank=True, null=True)
    at_id = models.CharField("AdasisTbox-ID ", max_length=50,blank=True, null=True)
    car_model = models.CharField("车型", max_length=50, blank=True, null=True)
    chassis_number = models.CharField("底盘号", unique=True, max_length=50)
    install_time = models.DateTimeField("安装时间", blank=True, null=True)
    device_remove_status = models.IntegerField("设备是否拆除:", choices=((0,"否"),(1,"是")), blank=True, null=True)
    device_remove_time = models.DateTimeField("拆除时间", blank=True, null=True)
    install_verion = models.CharField("安装版本号", max_length=50, blank=True, null=True)
    car_owner = models.IntegerField("车辆归属人",choices=((1,"个人"),(2,"车队")), blank=True, null=True)
    driver_name = models.CharField("归属人名称", max_length=50, blank=True, null=True)
    driver_phone = models.CharField("归属人联系方式", max_length=50, blank=True, null=True)
    driver_habit = models.IntegerField("驾驶员的驾驶习惯", choices=((1,"保守"),(2,"激进"),(3,"适中")), blank=True, null=True)
    speed_range = models.CharField("车速浮动区间", max_length=50, blank=True, null=True)
    other_remark = models.CharField("其他备注", max_length=255, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'pcc_vehicle_info'
        verbose_name = 'pcc车辆信息'
        verbose_name_plural = 'pcc车辆信息管理'

class DimSrc(models.Model):
    """
    车厂标记管理
    """

    depotLogo = models.IntegerField('车厂标记')
    src = models.CharField('车厂标识英文名称', max_length=10)
    src_chname = models.CharField('车厂标识中文名称', max_length=10)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField('编辑时间', auto_now=True, auto_now_add=False, blank=True, null=True)

    class Meta:
        db_table = 'dim_src'
        verbose_name = '车厂标记管理'
        verbose_name_plural = '车厂标记管理'



class HiveTableInfo(models.Model):
    tbl_id = models.IntegerField(primary_key=True)
    tbl_name = models.CharField('表名称',max_length=100, blank=True, null=True)
    db_id = models.IntegerField('数据库id',blank=True, null=True)
    db_name = models.CharField('数据库名称',max_length=100, blank=True, null=True)
    tbl_type = models.CharField('表类型',max_length=25, blank=True, null=True)
    tbl_owner = models.CharField('表所有者',max_length=25, blank=True, null=True)
    create_time = models.CharField('表创建时间',max_length=25, blank=True, null=True)
    is_online = models.IntegerField('是否在线',choices=((0,'下线'),(1,'上线')),blank=True, null=True)
    offline_time = models.CharField('下线时间',max_length=25, blank=True, null=True)
    update_time = models.CharField('更新时间',max_length=25, blank=True, null=True)
    location = models.CharField('存储地址',max_length=500, blank=True, null=True)
    partition = models.CharField('分区字段',max_length=100, blank=True, null=True)
    tbl_comment = models.CharField('表注释',max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.tbl_name

    class Meta:
        managed = False
        db_table = 'hive_table_info'
        verbose_name = 'hive表元数据管理'
        verbose_name_plural = 'hive表元数据管理'


class HiveTableMaintain(models.Model):
    id = models.IntegerField(primary_key=True)
    db_name = models.CharField('数据库名称',max_length=50, blank=True, null=True)
    table_name = models.CharField('表名称',max_length=100, blank=True, null=True)
    table_desc_maintain = models.CharField('表注释',max_length=100, blank=True, null=True)
    usage_desc = models.TextField('使用描述',max_length=1000,blank=True,null=True)
    create_time = models.CharField('表创建时间',max_length=25, blank=True, null=True)

    def __unicode__(self):
        return self.table_name

    class Meta:
        managed = False
        db_table = 'hive_table_maintain'
        verbose_name = 'hive表注释管理'
        verbose_name_plural = 'hive表注释管理'

class HiveTableColumnInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    column_id = models.CharField('字段id',max_length=50, blank=True, null=True)
    cd_id = models.IntegerField('元数据字段id',blank=True, null=True)
    integer_idx = models.IntegerField('字段排序',blank=True, null=True)
    column_name = models.CharField('字段名称',max_length=100, blank=True, null=True)
    column_type = models.CharField('字段类型',max_length=100, blank=True, null=True)
    column_desc = models.CharField('字段描述',max_length=100, blank=True, null=True)
    tbl_id = models.IntegerField('表id',blank=True, null=True)
    table_name = models.CharField('表名称',max_length=100, blank=True, null=True)
    db_id = models.IntegerField('数据库id',blank=True, null=True)
    db_name = models.CharField('数据库名称',max_length=50, blank=True, null=True)

    create_time = models.CharField('创建时间',max_length=25, blank=True, null=True)


    #table_name = models.ForeignKey('HiveTableInfo', db_column='tbl_name', verbose_name='表id')
    #db_name = models.ForeignKey('HiveTableInfo', db_column='db_name', verbose_name='数据库名称')

    def __unicode__(self):
        return self.column_name

    class Meta:
        managed = False
        db_table = 'hive_table_column_info'
        verbose_name = 'hive表字段管理'
        verbose_name_plural = 'hive表字段管理'

class HiveColumnMaintain(models.Model):
    id = models.IntegerField(primary_key=True)
    db_name = models.CharField('数据库名称',max_length=50, blank=True, null=True)
    table_name = models.CharField('表名称',max_length=100, blank=True, null=True)
    column_idx = models.IntegerField('字段排序',blank=True, null=True)
    column_desc_maintain = models.CharField('字段描述',max_length=200, blank=True, null=True)
    create_time = models.CharField('创建时间',max_length=25, blank=True, null=True)

    def __unicode__(self):
        return self.column_desc_maintain

    class Meta:
        managed = False
        db_table = 'hive_column_maintain'
        verbose_name = 'hive表字段维护'
        verbose_name_plural = 'hive表字段维护'

class MakefileTagRelations(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.CharField('表名称',max_length=100, blank=True, null=True)
    tag_rely = models.CharField('表依赖',max_length=100, blank=True, null=True)
    source = models.IntegerField('来源', null=True)
    scheduling = models.CharField('字段描述',max_length=100, blank=True, null=True)
    host = models.CharField('host',max_length=25, blank=True, null=True)

    def __unicode__(self):
        return self.tag

    class Meta:
        managed = False
        db_table = 'makefile_tag_relations_test'

## hive表索引
class HiveSearchIndex(models.Model):
    id = models.IntegerField(primary_key=True)
    db_id = models.IntegerField('数据库id',blank=True, null=True)
    db_name = models.CharField('数据库名称',max_length=255, blank=True, null=True)

    table_id = models.IntegerField('表id',blank=True, null=True)
    table_name = models.CharField('表名称',max_length=255, blank=True, null=True)
    table_name_split = models.CharField('表名称',max_length=255, blank=True, null=True)
    is_online = models.IntegerField('是否上线',blank=True, null=True)

    column_names = models.CharField('列名称',max_length=255, blank=True, null=True)
    column_names_split = models.CharField('列名称拆分',max_length=255, blank=True, null=True)

    table_content = models.CharField('表描述',max_length=255, blank=True, null=True)
    column_content = models.CharField('列描述',max_length=255, blank=True, null=True)
    table_sort_priority = models.IntegerField('表排序id',blank=True, null=True)
    create_time = models.CharField('创建时间',max_length=25, blank=True, null=True)
    update_time = models.CharField('修改时间',max_length=25, blank=True, null=True)


    def __unicode__(self):
        return self.table_name

    class Meta:
        managed = False
        db_table = 'hive_search_index'

    # 获取截取的列信息
    def getSubstrString(self,column, searchKey):
        columnArr = column.split(',')
        flag = 0
        index = 0
        # print(len(columnArr))
        if len(columnArr) > 0:
            for val in columnArr:
                matchObj = re.search(r'%s' % (searchKey), val, re.M | re.I)
                if matchObj:
                    break
                else:
                    pass
                    # print "No match!!"
                index = index + 1
        # print(index)
        if index == len(columnArr):
            return ','.join(columnArr[0:20])
        else:
            if len(columnArr) < 10:
                return ','.join(columnArr)
            else:
                start = index - 5
                if start < 0:
                    start = 0
                return ','.join(columnArr[start:index + 15])


#hive表浏览记录
class HiveSearchLog(models.Model):
    # id = models.IntegerField(primary_key=True)
    index_id = models.IntegerField('索引表id',blank=True, null=True)
    db_name = models.CharField('数据库名称',max_length=255, blank=True, null=True)
    table_name = models.CharField('表名称',max_length=255, blank=True, null=True)
    author_id = models.IntegerField('浏览人id',blank=True, null=True)
    create_time = models.CharField('浏览时间',max_length=255, blank=True, null=True)


    def __unicode__(self):
        return self.index_id

    class Meta:
        managed = False
        db_table = 'hive_search_log'

class HiveSearch(models.Model):

    class Meta:
        managed = False


class Detail(models.Model):

    class Meta:
        managed = False
        verbose_name = '详情'

#hive表空间存储
class HiveTableCapacity(models.Model):
    id = models.IntegerField(primary_key=True)
    tbl_id = models.IntegerField('表id',blank=True, null=True)
    storage = models.BigIntegerField('存储大小',blank=True, null=True)
    storage_unit = models.CharField('存储单位',max_length=10, blank=True, null=True)
    records = models.IntegerField('记录数',blank=True, null=True)
    last_ddl_time = models.IntegerField('最后修改时间',blank=True, null=True)
    calculate_date = models.DateField('计算日期',blank=True, null=True)
    storage_type = models.IntegerField('存储类型',blank=True, null=True)

    create_time = models.CharField('添加时间',max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hive_table_capacity'
        verbose_name = '表存储空间列表'
        verbose_name_plural = verbose_name

#hie数据质量规则表
class QualityRule(models.Model):
    rule_type_choice = (
        (1, '表级规则'),
        (2, '字段级规则'),
        (3, '自定义sql'),
    )

    check_type_choice = (
        (1, '数值型'),
        (2, '波动率型'),
    )

    check_mode_choice = (
        (1, '与固定值比较'),
        (2, '与昨天对比'),
        (3, '7天平均值对比'),
        (4, '30天平均值对比'),
    )

    execute_type_choice = (
        (1, '系统统一时间执行'),
        (2, '自定义时间执行'),
    )


    id = models.IntegerField(primary_key=True)
    rule_name = models.CharField('规则名称',max_length=50, blank=True, null=True)
    rule_type = models.IntegerField('规则类型',choices=rule_type_choice, null=True)
    db_name = models.CharField('数据库名',max_length=50, blank=True, null=True)
    table_name = models.CharField('表名',max_length=200, blank=True, null=True)
    column_name = models.CharField('列名',max_length=100, blank=True, null=True)
    custom_sql = models.CharField('自定义sql',max_length=2000, blank=True, null=True)
    sampling_mode = models.CharField('采样方式',max_length=50, blank=True, null=True)
    filter_condition = models.CharField('过滤条件',max_length=100, blank=True, null=True)
    check_type = models.IntegerField('校验类型',choices=check_type_choice, null=True)
    compare_mode = models.CharField('比较方式',max_length=50, blank=True, null=True)
    check_mode = models.IntegerField('校验方式',choices=check_mode_choice, null=True)
    excepted_value = models.IntegerField('期望值', blank=True, null=True)
    percent_min = models.IntegerField('波动率', blank=True, null=True)
    rule_desc = models.CharField('规则描述',max_length=255, blank=True, null=True)
    status = models.CharField('上线状态',max_length=10, blank=True, null=True)
    warning_mode = models.IntegerField('报警方式', blank=True, null=True)
    warning_receiver = models.CharField('报警接收人',max_length=200, blank=True, null=True)

    execute_type = models.IntegerField('执行方式',choices=execute_type_choice, null=True)
    execute_hour = models.CharField('执行时间',max_length=20, blank=True, null=True)

    create_user = models.CharField('创建人',max_length=50, blank=True, null=True)

    create_time = models.DateTimeField('创建时间',max_length=50, blank=True, null=True)

    @staticmethod
    def get_sampling_mode_name(mode_type):
        if mode_type in ('mode_count','mode_sum','mode_avg','mode_max','mode_min'):
            return mode_type.replace('mode_','')
        elif mode_type in ('mode_null'):
            return '空值'
        elif mode_type in ('mode_zero'):
            return '0值'
        elif mode_type in ('mode_repeat'):
            return '重复值'
        elif mode_type in ('mode_custom'):
            return '自定义sql'

    @staticmethod
    def get_compare_mode_name(compare_mode):
        if compare_mode == 'gt':
            return '>'
        elif compare_mode == 'gte':
            return '>='
        elif compare_mode == 'lt':
            return '<'
        elif compare_mode == 'lte':
            return '<='
        elif compare_mode == 'equal':
            return '='
        elif compare_mode == 'nequal':
            return '!='
        elif compare_mode == 'rise':
            return '上升'
        elif compare_mode == 'decline':
            return '下降'
        elif compare_mode == 'abs':
            return '绝对值'

    def __unicode__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hive_quality_rule'
        verbose_name = '数据质量规则'
        verbose_name_plural = '数据质量规则'

class RuleExecuteLog(models.Model):
    status_choice = (
        (0, '未执行'),
        (1, '执行中'),
        (2, '执行完成'),
        (3, '触发预警'),
        (4, '执行错误'),
    )
    id = models.IntegerField(primary_key=True)
    rule_id = models.IntegerField('规则id',blank=True, null=True)
    status = models.IntegerField('执行状态', choices=status_choice,blank=True, null=True)
    error_msg = models.CharField('错误信息',max_length=2000, blank=True, null=True)
    start_time = models.DateTimeField('开始时间',blank=True, null=True)
    end_time = models.DateTimeField('结束时间',blank=True, null=True)
    execute_seconds = models.IntegerField('执行时长',blank=True, null=True)
    execute_sql = models.CharField('执行sql',max_length=2000, blank=True, null=True)


    create_time = models.CharField('添加时间',max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hive_rule_execute_log'
        verbose_name = '规则执行日志'
        verbose_name_plural = '规则执行日志'


#hive总空间大小
class TableStorage(models.Model):
    id = models.IntegerField(primary_key=True)
    file_dir = models.CharField('文件路径',max_length=100, blank=True, null=True)
    total_size = models.CharField('总容量大小',max_length=50, blank=True, null=True)

    used_size = models.CharField('已使用的空间大小',max_length=50, blank=True, null=True)
    use_percent = models.CharField('已使用的百分比',max_length=50, blank=True, null=True)
    calculate_date = models.DateField('统计日期',blank=True, null=True)
    create_time = models.DateTimeField('添加时间', blank=True, null=True)

    def __unicode__(self):
        return self.id

    @staticmethod
    def readable_file_size(bytes, precision):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
            if abs(bytes) < 1024.0:
                return '%s %s' % (format(bytes, '.%df' % precision), unit)
            bytes /= 1024.0
        return '%s %s' % (format(bytes, '.%df' % precision), 'Yi')

    @staticmethod
    def readable_file_size_list(bytes):
        if bytes:
            bytes = float(bytes)
            for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
                if abs(bytes) < 1024.0:
                    return [format(bytes, '.%df' % 2),unit]
                bytes /= 1024.0
            return [format(bytes, '.%df' % 2),unit]
        else:
            return [0,'']

    class Meta:
        managed = False
        db_table = 'hive_table_all_storage'
        verbose_name = 'HIVE存储空间'
        verbose_name_plural = 'HIVE存储空间'


# 表规范
class TableStandard(models.Model):

    class Meta:
        managed = False
        verbose_name = '数据表规范'

# 字段规范
class FieldStandard(models.Model):

    class Meta:
        managed = False
        verbose_name = '字段名称规范'

# 表规范
class QualityTrend(models.Model):

    class Meta:
        managed = False
        verbose_name = '质量详情'

class Dict(models.Model):

    class Meta:
        managed = False
        verbose_name = '数据字典'

# 词根汇总
class WordSummary(models.Model):

    class Meta:
        managed = False
        verbose_name = '词根汇总'

#hive表数据示例
class TableExample(models.Model):
    id = models.IntegerField(primary_key=True)
    tbl_id = models.IntegerField('表id',blank=True, null=True)
    column_field = models.CharField('列字段',max_length=2000, blank=True, null=True)
    column_data = models.TextField('列数据',max_length=5000, blank=True, null=True)
    create_time = models.DateTimeField('添加时间', blank=True, null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hive_table_example'
        verbose_name = 'HIVE表数据示例'
        verbose_name_plural = 'HIVE表数据示例'

#hive表数据示例
class HiveTableExtend(models.Model):
    id = models.IntegerField(primary_key=True)
    tbl_id = models.IntegerField('表id',blank=True, null=True)

    storage_format = models.CharField('存储格式',max_length=50, blank=True, null=True)
    compression = models.CharField('压缩格式',max_length=50, blank=True, null=True)
    last_ddl_time = models.DateTimeField('ddl更新时间', blank=True, null=True)
    create_time = models.DateTimeField('添加时间', blank=True, null=True)
    update_time = models.DateTimeField('更新时间', blank=True, null=True)


    def __unicode__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hive_table_extend'
        verbose_name = 'HIVE信息扩展表'
        verbose_name_plural = 'HIVE信息扩展表'

#用户组织表
class HiveOrgInfo(models.Model):
    #id = models.IntegerField(primary_key=True)

    name = models.CharField('组织名称',max_length=100, blank=False, unique=True, null=False)
    create_time = models.DateTimeField('添加时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'hive_org_info'
        verbose_name ='组织'
        verbose_name_plural = '组织'


#用户组织表
class HiveOwnerOrg(models.Model):
    #id = models.IntegerField(primary_key=True)

    owner_name = models.CharField('用户名称',max_length=100, blank=False, unique=True, null=False)
    #org_id = models.IntegerField('组织id',default=0,null=False)

    org_id = models.ForeignKey("HiveOrgInfo",db_column='org_id',on_delete=models.CASCADE,verbose_name="归属组织")
    create_time = models.DateTimeField('添加时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


    class Meta:
        managed = False
        db_table = 'hive_owner_org'
        verbose_name ='用户组织关系'
        verbose_name_plural = '用户组织关系'

        unique_together = ('owner_name', 'org_id',)

# 表存储排行
class StorageRanking(models.Model):

    class Meta:
        managed = False
        verbose_name = '表存储排行'

# 用户资产信息
class UserStorage(models.Model):

    class Meta:
        managed = False
        verbose_name = '用户资产信息'

# 用户组织表
class UserOrgTable(models.Model):

    class Meta:
        managed = False
        verbose_name = '用户组织表存储空间'
