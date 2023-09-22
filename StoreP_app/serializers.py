from rest_framework import serializers
from .models import Store_status, Store_Business_Hour, Store_Timezone, Report


class Report_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("store", "report_status", "report_url")

    report_id = serializers.IntegerField()


class Store_Timezone_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Store_Timezone
        fields = ("store_id", "timezone_str")


class Store_status_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Store_status
        fields = ("store", "status", "timestamp_utc")


class Store_Business_Hour_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Store_Business_Hour
        fields = ("store", "dayOfWeek", "start_time_local", "end_time_local")
