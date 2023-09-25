from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from StoreP_app.models import Store_Timezone, Report, report_status
from .serializers import Report_Serializer
from StoreP_app.populate_data import generate_report, generate_csv_file
from .populate_data import trigger_report
from django.conf import settings


class RestroViewSet(ModelViewSet):
    queryset = Store_Timezone.objects.all()
    serializer_class = Report_Serializer

    @action(
        detail=True,
        methods=["GET"],
    )
    def trigger_report(self, request, pk=None):
        restro = self.get_object()
        report = Report.objects.create(restro=restro, status=report_status.PENDING)
        csv_data = []
        data = generate_report(restro)
        csv_data.append(data)
        generate_csv_file(report, csv_data)
        return Response(status=200, data={"report_id": report.id})

    @action(
        detail=False,
        methods=["POST"],
    )
    def get_report(self, request):
        report_id = request.data.get("report_id")
        report = get_object_or_404(Report, id=report_id)
        if report.status == report_status.COMPLETED:
            report_url = settings.MEDIA_ROOT + "/" + report.report_url.name
            with open(report_url, "rb") as csv_file:
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
        if self.action == "trigger_report":
            return Report_Serializer
        return super().get_serializer_class()
