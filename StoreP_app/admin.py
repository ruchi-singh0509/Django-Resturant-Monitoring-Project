from django.contrib import admin
from .models import Store_status, Store_Business_Hour, Store_Timezone,Report

# Register your models here.
admin.site.register(Store_Timezone)
class Store_Timezone_Admin(admin.ModelAdmin):
    list_display = ("store_id","timezone")
    list_filter=("timezone",)
    search_field=("store_id",)
admin.site.register(Store_Business_Hour)
class Store_Business_Hour_Admin(admin.ModelAdmin):
    list_display=("store","dayOfWeek","start_time","end_time")
    raw_id_fields= ("store",)
    list_filter=("dayOfWeek",)
    search_field=("store_id",)

admin.site.register(Store_status)
class Store_status_Admin(admin.ModelAdmin):
    list_display = ("store","status","timestamp_utc")
    raw_id_fields =("store",)
    list_filter = ("status",)
    search_field = ("store_id",)

admin.site.register(Report)
class Report_Admin(admin.ModelAdmin):
    list_display=("store","report_status","report_url")
    raw_id_fields=("store",)
    list_filter=("report_status")
    search_field=("store_id")


