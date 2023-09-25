from django.contrib import admin
from .models import Store_status, Store_Business_Hour, Store_Timezone, Report

# Register your models here.
admin.site.register(Store_Timezone)


class Store_Timezone_Admin(admin.ModelAdmin):
    list_display = ("store_id", "timezone_str")
    list_filter = ("timezone_str",)
    search_field = ("store_id",)


admin.site.register(Store_Business_Hour)


class Store_Business_Hour_Admin(admin.ModelAdmin):
    list_display = ("restro", "dayOfWeek", "start_time", "end_time")
    raw_id_fields = ("restro",)
    list_filter = ("dayOfWeek",)
    search_field = ("store_id",)


admin.site.register(Store_status)


class Store_status_Admin(admin.ModelAdmin):
    list_display = ("restro", "status", "timestamp_utc")
    raw_id_fields = ("restro",)
    list_filter = ("status",)
    search_field = ("store_id",)


admin.site.register(Report)


class Report_Admin(admin.ModelAdmin):
    list_display = ("restro", "status", "report_url")
    raw_id_fields = ("restro",)
    list_filter = ("status",)
    search_field = ("store_id",)
