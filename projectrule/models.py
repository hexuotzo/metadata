from django.db import models


class ProjectFirstType(models.Model):
    '''
    项目大类管理
    '''
    name = models.CharField('分类名', max_length=100, unique=True)
    code = models.CharField('编码', max_length=100, unique=True)
    creator = models.CharField('创建人', max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return "%s: %s" % (self.code, self.name)
    
    def set_code(self):
        '''
        生成规则: 每个一级类目下的二级类目id递增, 取四位补0.
        '''
        lastid = ProjectFirstType.objects.all()
        lastid = lastid and int(lastid.latest('code').code) or 0
        if self.pk:   # 只在新建时生成tid, 编辑时不能更新
            return False
        self.code = "%02d" % (lastid + 1)
    
    class Meta:
        verbose_name = '项目大类'
        verbose_name_plural = "项目大类管理"
        

class ProjectsCustomerAndProductType(models.Model):
    '''
    客户与产品类型管理 (二级类目)
    '''
    project = models.ForeignKey(ProjectFirstType, on_delete=models.CASCADE)
    name =  models.CharField('客户与产品类型', max_length=100,unique=True)
    shortname = models.CharField('简称', max_length=100,unique=True)
    code = models.CharField('分类编码', max_length=100)
    full_code = models.CharField('完整分类编码', max_length=100, unique=True)
    creator = models.CharField('创建人', max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)
    
    def set_code(self):
        '''
        生成规则: 每个一级类目下的二级类目id递增, 取四位补0.
        '''
        lastid = ProjectsCustomerAndProductType.objects.filter(
            project=self.project)
        lastid = lastid and int(lastid.latest('code').code) or 0
        if self.pk:   # 只在新建时生成tid, 编辑时不能更新
            return False
        self.code = "%04d" % (lastid + 1)
        self.full_code = "%02d%s" % (int(self.project.code), self.code)
    
    class Meta:
        verbose_name = '客户/产品类型'
        verbose_name_plural = "客户/产品类型管理"
        
    def __str__(self):
        return "%s: %s - %s" % (self.full_code, self.project.name, self.shortname)
    
    
class ZHProductManage(models.Model):
    '''
    产品管理
    '''
    product_type = models.ForeignKey(ProjectsCustomerAndProductType, on_delete=models.CASCADE)
    name =  models.CharField('产品名称', max_length=100)
    product_desc = models.TextField('说明', blank=True)
    
    creator = models.CharField('创建人', max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)
    
    class Meta:
        verbose_name = '中寰项目管理'
        verbose_name_plural = "中寰项目管理"
        
    def __str__(self):
        return self.name