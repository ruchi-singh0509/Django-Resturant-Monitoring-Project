from rest_framework import serializers
from StoreP_app.models import Report

__all__ = ["Report_Serializer"]


class Report_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["report_id"]

    report_id = serializers.IntegerField()
