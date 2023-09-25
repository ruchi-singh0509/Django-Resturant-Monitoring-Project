from StoreP_app.models import Store_status, store_status, Report, report_status
from django.utils import timezone
from pytz import timezone as pytz_timezone
import datetime
from StoreP_app.models import Store_Timezone

restros = Store_Timezone.objects.all()[:50]
from StoreP_app.populate_data import trigger_report

report = Report.objects.create(status=report_status.PENDING)
trigger_report(report)
