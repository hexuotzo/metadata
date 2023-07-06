from django.contrib import admin

from projectrule.models import ProjectFirstType, ProjectsCustomerAndProductType, ZHProductManage

class ProjectFirstTypeAdmin(admin.ModelAdmin):
    
    list_display = ['code', 'name', 'create_time']
    search_fields = ['name',]
    list_filter = ['create_time', ]
    readonly_fields = ('creator', 'create_time')
    ordering = ('code',)
    
    def save_model(self, request, obj, form, change):
        obj.set_code()
        if not obj.id:
            obj.creator = request.user.username
        obj.save()

admin.site.register(ProjectFirstType, ProjectFirstTypeAdmin)

class ProjectsCustomerAndProductTypeAdmin(admin.ModelAdmin):
    
    list_display = ['full_code', 'shortname', 'name', 'project_name', 'create_time']
    search_fields = ['name','shortname','full_code']
    list_filter = ['create_time', ]
    readonly_fields = ('code', 'full_code', 'creator', 'create_time')
    ordering = ('code',)
    
    def project_name(self, obj):
        return obj.project.name
    project_name.short_description ='分类名称'
    
    def save_model(self, request, obj, form, change):
        obj.set_code()
        if not obj.id:
            obj.creator = request.user.username
        obj.save()

admin.site.register(ProjectsCustomerAndProductType, ProjectsCustomerAndProductTypeAdmin)

class ZHProductManageAdmin(admin.ModelAdmin):
    
    list_display = ['product_fullname', 'product_type_code', 'product_type_name', 'product_type_shortname','create_time']
    search_fields = ['name',]
    list_filter = ['create_time', ]
    readonly_fields = ('creator', 'create_time')
    
    def product_fullname(self, obj):
        return "%s-%s-%s" % (obj.product_type.project.name, obj.product_type.shortname, obj.name)
    product_fullname.short_description ='项目名称'
    
    def product_type_code(self, obj):
        return obj.product_type.full_code
    product_type_code.short_description ='项目分类编码'
    
    def product_type_name(self, obj):
        return obj.product_type.name
    product_type_name.short_description ='项目分类名称'
    
    def product_type_shortname(self, obj):
        return obj.product_type.shortname
    product_type_shortname.short_description ='项目分类简称'
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creator = request.user.username
        obj.save()

admin.site.register(ZHProductManage, ZHProductManageAdmin)