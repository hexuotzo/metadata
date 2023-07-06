# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group

from usertags.models import Tags, UserTagsClient
from videotags.models import VideoTags


class PermUserTags(models.Model):
    group = models.ForeignKey(Group)
    tags = models.ManyToManyField(Tags, verbose_name=u'用户标签')

    class Meta:
        verbose_name = u'用户标签权限'
        verbose_name_plural = u'用户标签权限'
    
    def __unicode__(self):
        return self.group.name


# class PermVideoTags(models.Model):
#     group = models.ForeignKey(Group)
#     tags = models.ManyToManyField(VideoTags, verbose_name=u'视频标签')

#     class Meta:
#         verbose_name = u'视频标签权限'
#         verbose_name_plural = u'视频标签权限'
    
#     def __unicode__(self):
#         return self.group.name
        

class PermUserClient(models.Model):
    group = models.ForeignKey(Group)
    client = models.ManyToManyField(UserTagsClient, verbose_name=u'客户端')

    class Meta:
        verbose_name = u'客户端数据查询权限'
        verbose_name_plural = u'客户端数据查询权限'
    
    def __unicode__(self):
        return self.group.name


class GroupDesc(models.Model):
    group = models.OneToOneField(Group)
    desc = models.TextField('角色说明', default='')
    crowd = models.TextField('角色适用人群', default='')
    
    class Meta:
        verbose_name = u'角色说明'
    
    def __unicode__(self):
        return self.group.name