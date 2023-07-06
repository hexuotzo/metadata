from django.db import models

class LbldataBusinessInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_id = models.BigIntegerField("数据包id",blank=True, null=True)
    dir_name = models.CharField("目录名称",max_length=255, blank=True, null=True)
    dir_path = models.CharField("目录地址",max_length=255, blank=True, null=True)
    dir_describe = models.CharField("目录数据业务描述",max_length=255, blank=True, null=True)
    data_multi_type = models.CharField("目录数据种类",max_length=255, blank=True, null=True)
    create_time = models.DateTimeField("创建时间",blank=True, null=True,auto_now_add=True)
    update_time = models.DateTimeField("更新时间",blank=True, null=True, auto_now=True)


    def __str__(self):
        return "标注数据业务信息梳理表"

    class Meta:
        verbose_name = "标注数据业务信息梳理表"
        verbose_name_plural = "标注数据业务信息梳理表"
        managed = False
        db_table = 'lbldata_business_info'


class DimSource(models.Model):
    source = models.CharField("数据来源",max_length=255, blank=True, null=True)
    source_short = models.CharField("数据来源简称",max_length=255, blank=True, null=True)
    source_describe = models.CharField("数据来源描述",max_length=255, blank=True, null=True)
    create_time = models.DateTimeField("创建时间",blank=True, null=True,auto_now_add=True)
    update_time = models.DateTimeField("更新时间",auto_now=True)

    def __str__(self):
        return "数据来源字典表"

    class Meta:
        verbose_name = '数据来源字典表'
        verbose_name_plural = '数据来源字典表'
        managed = False
        db_table = 'dim_source'


class DimElementCode(models.Model):
    element_id = models.IntegerField("要素id",unique=True)
    element_name = models.CharField("要素名称",max_length=255)
    map_column = models.CharField("映射字段",max_length=255)
    excute_batch = models.IntegerField("执行批次号",)
    limit_condition = models.CharField("筛选条件",max_length=255, blank=True, null=True)
    create_time = models.DateTimeField("创建时间",blank=True, null=True,auto_now_add=True)
    update_time = models.DateTimeField("更新时间",blank=True, null=True,auto_now=True)

    def __str__(self):
        return "图片要素字典表"

    class Meta:
        verbose_name = "图片要素字典表"
        verbose_name_plural = "图片要素字典表"
        managed = False
        db_table = 'dim_element_code'


class DimTraitCode(models.Model):
    trait_id = models.IntegerField("特征id",unique=True)
    trait_name = models.CharField("特征名称",max_length=255)
    create_time = models.DateTimeField("创建时间",blank=True, null=True,auto_now_add=True)
    update_time = models.DateTimeField("更新时间",blank=True, null=True,auto_now=True)

    def __str__(self):
        return "特征字典表"

    class Meta:
        verbose_name = "特征字典表"
        verbose_name_plural = "特征字典表"
        managed = False
        db_table = 'dim_trait_code'


class ElementDataBatch(models.Model):
    data_type = models.CharField("数据类型",max_length=255)
    source = models.CharField("数据源",max_length=255)
    source_data_id = models.CharField("数据集id",max_length=255)
    pdt = models.CharField("数据批次号",max_length=255)
    source_ch = models.CharField("数据源中文",max_length=255, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", blank=True, null=True,auto_now_add=True)
    update_time = models.DateTimeField("更新时间",blank=True, null=True,auto_now=True)

    def __str__(self):
        return "要素有效检出数据批次表"

    class Meta:
        verbose_name = "要素有效检出数据批次表"
        verbose_name_plural = "要素有效检出数据批次表"
        managed = False
        db_table = 'element_data_batch'


class DimMeshElement(models.Model):
    id = models.BigAutoField(primary_key=True)
    element_code = models.CharField("要素id",unique=True, max_length=100, blank=True, null=True)
    element_name = models.CharField("要素名称",max_length=100, blank=True, null=True)
    map_column = models.CharField("映射字段",max_length=100, blank=True, null=True)
    excute_batch = models.IntegerField("执行批次号",blank=True, null=True)
    limit_condition = models.CharField("限制条件",max_length=100, blank=True, null=True)
    create_time = models.DateTimeField("创建时间",max_length=50, blank=True, null=True,auto_now_add=True)
    update_time = models.DateTimeField("更新时间",max_length=50, blank=True, null=True,auto_now=True)
    pdt = models.CharField("数据录入日期",max_length=10, blank=True, null=True)

    def __str__(self):
        return "Tile要素字典表"

    class Meta:
        verbose_name = "Tile要素字典表"
        verbose_name_plural = "Tile要素字典表"
        managed = False
        db_table = 'dim_mesh_element'


