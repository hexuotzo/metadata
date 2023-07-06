# -*- coding: utf-8 -*-

from django.db.models import ManyToManyField, TextField
from django.contrib import auth, admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.models import LogEntry
from django.core.exceptions import ObjectDoesNotExist
from common.models.perm_models import PermUserTags, GroupDesc, PermUserClient
from usertags.params import ACTION_FLAG_NAME

AdminSite.site_title = '标签管理后台'
AdminSite.site_header = '标签管理后台'
AdminSite.site_url = '/'


class ActionFlagFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '用户操作记录'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'action_flag_name'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        return ACTION_FLAG_NAME

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(action_flag=self.value())


class LogAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'object_repr', 'content_type', 'change_message', 'action_time')
    list_filter = ('action_time', ActionFlagFilter)
    search_fields = ['user__username', 'change_message', 'object_repr']
    readonly_fields = ('user', 'content_type', 'object_repr',
                       'change_message', 'action_time', 'action_flag', 'object_id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PermUserTagsInline(admin.StackedInline):
    fieldsets = (
        ("", {
            'fields': (('tags', ),)
        }),
    )
    model = PermUserTags
    extra = 1
    max_num = 1
    can_delete = True
    verbose_name = '用户标签权限'
    verbose_name_plural = '用户标签权限设置'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ManyToManyField):
            kwargs['widget'] = admin.widgets.FilteredSelectMultiple(
                verbose_name='', is_stacked=False)

        return super(PermUserTagsInline, self).formfield_for_dbfield(db_field, **kwargs)


# class PermVideoTagsInline(admin.StackedInline):
#     fieldsets = (
#         ("", {
#             'fields': (('tags', ),)
#         }),
#     )
#     model = PermVideoTags
#     extra = 1
#     max_num = 1
#     can_delete = True
#     verbose_name = '视频标签权限'
#     verbose_name_plural = '视频标签权限设置'

#     def formfield_for_dbfield(self, db_field, **kwargs):
#         if isinstance(db_field, ManyToManyField):
#             kwargs['widget'] = admin.widgets.FilteredSelectMultiple(
#                 verbose_name='', is_stacked=False)

#         return super(PermVideoTagsInline, self).formfield_for_dbfield(db_field, **kwargs)


class PermUserClientInline(admin.StackedInline):
    fieldsets = (
        ("", {
            'fields': (('client', ),)
        }),
    )
    model = PermUserClient
    extra = 1
    max_num = 1
    can_delete = True
    verbose_name = '客户端数据查询权限'
    verbose_name_plural = '客户端数据查询权限设置'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ManyToManyField):
            kwargs['widget'] = admin.widgets.FilteredSelectMultiple(
                verbose_name='', is_stacked=False)

        return super(PermUserClientInline, self).formfield_for_dbfield(db_field, **kwargs)
        

class GroupDescInline(admin.StackedInline):
    model = GroupDesc
    can_delete = False
    verbose_name_plural = '角色说明设置'


class GroupAdmin(auth.admin.GroupAdmin):
    inlines = (GroupDescInline,
               PermUserClientInline,
               PermUserTagsInline)

    formfield_overrides = {ManyToManyField: {'widget': admin.widgets.FilteredSelectMultiple(verbose_name='', is_stacked=False)}
                           }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ManyToManyField):
            kwargs['widget'] = admin.widgets.FilteredSelectMultiple(
                verbose_name='', is_stacked=False)
        if isinstance(db_field, TextField):
            return forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 3, 'class': 'docx'}), label='描述')
        return super(GroupAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        if 'permissions' in form.base_fields:
            permissions = form.base_fields['permissions']
            permissions.queryset = permissions.queryset.filter(content_type__app_label__in=['admin', 'auth', 'usertags', 'videotags'])
        return form


class UserAdmin(auth.admin.UserAdmin):
    list_display = ('username', 'email', 'full_name', 'groupname', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ['username', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': 
            ('username', 'password')}), 
        (u'Personal info', 
            {'fields': 
                ('first_name', 'last_name', 'email')}), 
        (u'Permissions', 
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}), 
        (u'Important dates', 
            {'fields': ('last_login', 'date_joined')}))

    def full_name(self, obj):
        return "%s%s" % (obj.last_name, obj.first_name)
    full_name.short_description = '姓名'
    
    def groupname(self, obj):
        return obj.groups.first()
    groupname.short_description = '角色名称'
    
    def save_model(self, request, obj, form, change):
        '''
        属于管理员组的用户, 自动设置为超级用户
        '''
        
        try:
            g = Group.objects.get(name='管理员组')
        except ObjectDoesNotExist:
            return obj.save()
            
        if unicode(g.id) in form.data.getlist('groups'):
            obj.is_superuser = True
        obj.save()
        
    class Media:
        js = ("/static/js/jquery-3.2.1.min.js",
            "/static/js/api_random_secret.js",)
    

def permission_unicode(self):
    return u"%s: %s" % (self.content_type.name, self.name)


Permission.__unicode__ = permission_unicode
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.unregister(auth.models.Group)
admin.site.register(auth.models.Group, GroupAdmin)

admin.site.register(LogEntry, LogAdmin)