from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Store_Timezone, Report
from .serializers import Report_Serializer
from rest_framework.response import Response
from StoreP_app.populate_data import generate_report, generate_csv_file, trigger_report
from django.conf import settings

import pdb

pdb.set_trace()


class StoreViewSet(ModelViewSet):
    queryset = Store_Timezone.objects.all()

    @action(detail=False, methods=["GET"], url_path="trigger_report")
    def trigger_report(self, request, pk=None):
        store = self.get_object()
        report = Report.objects.create(store=store, status="Pending")
        csv_data = []
        data = generate_report(store)
        csv_data.append(data)
        generate_csv_file(report, csv_data)
        return Response(status=200, data={"report_id": report.pk})

    @action(detail=False, methods=["GET"], url_path="get_report")
    def get_report(self, request):
        report_id = request.data.get("report_id")
        report = Report.objects.get(pk=report_id)

        serializer = Report_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = Report.DoesNotExist(Report, id=report_id)
        if report.status == Report.report_status.COMPLETED:
            report_url = Report.report_url.url
            with open(report_url.path, "rb") as csv_file:
                csv_data = csv_file.readlines()
                return Response(
                    status=200,
                    data={
                        "report_url": report_url,
                        "status": "Complete",
                        "csv_data": csv_data,
                    },
                )
        else:
            return Response(status=200, data={"status": "Running"})

    def get_serializer_class(self):
        if self.action == "get_report":
            return Report_Serializer
        return super().get_serializer_class()
