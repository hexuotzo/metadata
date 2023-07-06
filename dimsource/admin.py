from django.contrib import admin
from dimsource.models import *
# Register your models here.


class LbldataBusinessInfoAdmin(admin.ModelAdmin):
    list_display = ("data_id", "dir_name", "dir_path", "dir_describe", "data_multi_type", "create_time", "update_time")
    fields = ("data_id", "dir_name", "dir_path", "dir_describe", "data_multi_type")
    search_fields = ("data_id","dir_name")

admin.site.register(LbldataBusinessInfo, LbldataBusinessInfoAdmin)


class DimSourceAdmin(admin.ModelAdmin):
    list_display = ("source", "source_short", "source_describe", "create_time", "update_time")
    fields = ("source", "source_short", "source_describe")
    search_fields = ("source","source_describe")

admin.site.register(DimSource, DimSourceAdmin)

@admin.register(DimElementCode)
class DimElementCodeAdmin(admin.ModelAdmin):
    list_display = ("element_id", "element_name", "map_column", "excute_batch", "limit_condition", "create_time", "update_time",)
    fields = ("element_id", "element_name", "map_column", "excute_batch", "limit_condition")
    search_fields = ("element_name", "map_column")

@admin.register(DimTraitCode)
class DimTraitCodeAdmin(admin.ModelAdmin):
    list_display = ("trait_id", "trait_name", "create_time", "update_time",)
    fields = ("trait_id", "trait_name")
    search_fields = ("trait_name",)

@admin.register(ElementDataBatch)
class ElementDataBatchAdmin(admin.ModelAdmin):
    list_display = ("data_type", "source", "source_data_id", "pdt", "source_ch", "create_time", "update_time",)
    fields = ("data_type", "source", "source_data_id", "pdt", "source_ch")
    search_fields = ("source", "source_data_id")


@admin.register(DimMeshElement)
class DimMeshElementAdmin(admin.ModelAdmin):
    list_display = ("element_code", "element_name", "map_column", "excute_batch", "limit_condition", "create_time", "update_time", "pdt")
    fields = ("element_code", "element_name", "map_column", "excute_batch", "limit_condition","pdt")
    search_fields = ("element_code", "element_name", "map_column", "excute_batch", "limit_condition")