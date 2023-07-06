# -*-coding:utf-8-*-
from io import BytesIO

from django.http import HttpResponse
import xlwt
class exportExcel(object):
    def download_excel(self, request, queryset):

        meta = self.model._meta.verbose_name
        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        content_type = 'attachment;filename=%s.xls' % (str(meta))
        response['Content-Disposition'] = content_type

        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('sheet0')


        # 写入文件标题
        i = 0
        for k in self.fields:
            sheet.write(0,i,k)
            i+=1
        # 写入数据
        j=1
        for val in queryset:
            k=0
            for attr in self.fields:
                if self.special_fields and self.special_fields.has_key(str(attr)):

                    func_obj = getattr(val,self.special_fields[str(attr)])
                    res = func_obj()
                else:
                    res = str(getattr(val,attr))
                sheet.write(j,k,res)
                k+=1
            j+=1
        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    download_excel.short_description = "导出excel"