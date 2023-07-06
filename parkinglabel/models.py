# -*- coding: utf-8 -*-

import json
import datetime

from collections import OrderedDict

from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import *

from usertags.common.models import TrimCharField, ItemInfo
from usertags.params import (CATEGORY_STAT, VALID_TIME, VALTYPES,
                             TAG_FREQ, KEY_USERTAGS, CHART_TYPE, TAG_STATUS_SETNEXT, BELONG_TO)


class ParkingFirstCategory(models.Model):
    name = TrimCharField(
        '一级分类名', max_length=100, default='')
    ename = TrimCharField(
        '一级分类英文名', max_length=100, default='')
    desc = TrimCharField(
        '新增说明', max_length=255, default='')
    stat = models.CharField('状态',
                            max_length=2, choices=CATEGORY_STAT, default='2')
    belong = models.CharField('标签主体', max_length=2, choices=BELONG_TO, default='1')
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True, auto_now_add=False)

    class Meta:
        db_table = "parking_usertags_firstcategory"
        verbose_name = "用户标签一级分类"
        verbose_name_plural = "用户标签一级分类"
        # permissions = (
        #     ("view_category", "分类操作-查看"),
        #     ("edit_category", "分类操作-编辑"),
        #     ("page_category", "分类管理页查看"),
        # )

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return u"%s" % self.name


class ParkingSecondCategory(models.Model):
    first_category = models.ForeignKey(ParkingFirstCategory, verbose_name='一级分类', on_delete=models.PROTECT, default=None)
    tid = TrimCharField('二级分类编码', max_length=255, default='')
    full_tid = TrimCharField('完整分类编码', max_length=25, default='', unique=True)
    name = TrimCharField(
        '二级分类名', max_length=100, default='')
    ename = TrimCharField(
        '二级分类英文名', max_length=100, default='')
    desc = TrimCharField(
        '新增说明', max_length=255, default='')
    stat = models.CharField('状态',
                            max_length=2, choices=CATEGORY_STAT, default='2')
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True, auto_now_add=False)

    def set_tid(self):
        '''
        生成规则: 每个一级类目下的二级类目id递增, 取三位补0.
        '''
        lastid = ParkingSecondCategory.objects.filter(
            first_category=self.first_category)
        lastid = lastid and int(lastid.latest('tid').tid) or 0
        if self.pk:  # 只在新建时生成tid, 编辑时不能更新
            return False
        self.tid = "%04d" % (lastid + 1)
        self.full_tid = "%03d_%s" % (self.first_category.pk, self.tid)

    def get_full_tid(self):
        return self.full_tid

    def save(self, *args, **kwargs):
        self.set_tid()
        super(ParkingSecondCategory, self).save(*args, **kwargs)

    def get_firstcategory_name(self):
        return self.first_category.name

    class Meta:
        verbose_name = "用户标签二级分类"
        verbose_name_plural = "用户标签二级分类"
        db_table = "parking_usertags_secondcategory"
        # permissions = (
        #     ("view_category", "分类操作-查看"),
        #     ("edit_category", "分类操作-编辑"),
        #     ("page_category", "分类管理页查看"),
        # )

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return u"%s_%s_%s" % (self.first_category.get_belong_display(), self.first_category.name, self.name)


class ParkingTags(models.Model):
    label_lv1_id = models.CharField('一级标签id', max_length=255, default='')
    label_lv1_name = models.CharField('一级标签中文名称', max_length=255, default='')
    label_lv1_name_en = models.CharField('一级标签英文名称', max_length=255, default='')
    label_lv2_id = models.ForeignKey(ParkingSecondCategory, to_field="full_tid", db_column="label_lv2_id",  # 去掉三级分类, 只用二级分类
                                     verbose_name='二级标签id', on_delete=models.PROTECT, default=None)
    label_lv2_name = models.CharField('二级标签中文名称', max_length=255, default='')
    label_lv2_name_en = models.CharField('二级标签英文名称', max_length=255, default='')
    label_id = TrimCharField('标签id', max_length=255, default='', unique=True)
    # label_full_tid = TrimCharField('完整标签编码', max_length=25, default='')
    label_name = TrimCharField(
        '标签名', max_length=100, default='')
    label_name_en = TrimCharField(
        '标签英文名', max_length=100, default='')
    label_class = models.CharField('标签主体', max_length=2, choices=BELONG_TO, default='1')
    # fcategory_id = models.IntegerField('一级类ID', blank=True, default=0)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True, auto_now_add=False)

    def set_label_id(self):
        '''
        生成规则: 每个类目下的标签id递增, 取五位补0.
        '''
        lastid = ParkingTags.objects.filter(
            label_lv2_id=self.label_lv2_id.get_full_tid())

        if lastid:
            lastid_full = lastid.latest('label_id').label_id
            lastid = lastid_full and int(lastid_full.split("_")[2]) or 0
        else:
            lastid = 0

        # if self.pk:  # 只在新建时生成tid, 编辑时不能更新
        #     return False

        self.label_id = "%s_%s" % (self.label_lv2_id.get_full_tid(), "%05d" % (lastid + 1))

    def valid_date(self):
        if self.validdays == '99999':
            return '永久'
        days = datetime.timedelta(int(self.validdays))
        return (self.createtime + days).strftime("%Y-%m-%d")

    # def get_full_tid(self):
    #     return self.label_full_tid

    def next_set_status(self):
        '''
        允许设置的下一状态
        '''
        return TAG_STATUS_SETNEXT.get(self.stat, [])

    def save(self, *args, **kwargs):
        old_data = ParkingTags.objects.filter(id=self.id).values("label_lv2_id").first()
        if not old_data or old_data['label_lv2_id'] != self.label_lv2_id.full_tid:  # 判断是否更改了label_id   如果更改了 就生成新的label_id  如果没有更改就不改变
            self.set_label_id()

        first_obj = self.label_lv2_id.first_category
        self.label_lv1_id = "%03d" % first_obj.id
        self.label_lv1_name = first_obj.name
        self.label_lv1_name_en = first_obj.ename
        second_obj = self.label_lv2_id
        self.label_lv2_name = second_obj.name
        self.label_lv2_name_en = second_obj.ename
        self.label_class = first_obj.belong
        # cache.delete(KEY_USERTAGS)
        super(ParkingTags, self).save(*args, **kwargs)


    class Meta:
        db_table = 'parking_label_base_info'
        verbose_name = "规则类标签"
        verbose_name_plural = "规则类标签"
        # permissions = (
        #     ("view_usertags_tags", "标签管理-查看"),
        #     ("edit_usertags_tags", "标签管理-编辑"),
        #     ("page_usertags_tags", "用户标签管理页面查看"),
        # )
        # unique_together = ['label_name_en', 'label_lv2_id']

    def __unicode__(self):
        return u"%s(编码: %s)" % (self.label_name, self.label_id)

    def __str__(self):
        return u"%s(编码: %s)" % (self.label_name, self.label_id)


class ParkingLabelBaseInfoExtend(models.Model):
    label_id = models.OneToOneField(ParkingTags, to_field="label_id", db_column="label_id",  # 去掉三级分类, 只用二级分类
                                    verbose_name='标签ID', on_delete=models.CASCADE)
    label_desc = models.TextField(
        '新增说明', default='', blank=True)
    label_stat = models.CharField('状态',
                                  max_length=2, choices=CATEGORY_STAT, default='4')
    validdays = models.CharField('有效期',
                                 max_length=5, choices=VALID_TIME, default=VALID_TIME[0][0])
    valtype = models.CharField('标签值类型',
                               max_length=1, choices=VALTYPES, default=VALTYPES[0][0])
    freq = models.CharField('更新频次',
                            max_length=1, choices=TAG_FREQ, default=TAG_FREQ[0][0])

    class Meta:
        db_table = 'parking_label_base_info_extend'
        verbose_name = "标签属性"
        verbose_name_plural = "标签属性"

    def __str__(self):
        return self.label_id.label_id




class ParkingLabelElementCustomValue(models.Model):
    label_id = models.ForeignKey(ParkingTags, to_field="label_id", db_column="label_id", on_delete=models.CASCADE,
                                 verbose_name='标签id')
    label_value = models.CharField("标签值", max_length=255)
    label_desc = models.CharField("标签描述", max_length=255)
    create_time = models.DateTimeField("创建时间", blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField("更新时间", blank=True, null=True, auto_now=True)

    def __str__(self):
        return "标签值需求描述"

    class Meta:
        verbose_name = "标签值需求描述"
        verbose_name_plural = "标签值需求描述"
        db_table = "parking_label_element_custom_value"
