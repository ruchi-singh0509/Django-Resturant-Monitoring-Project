from StoreP_app.models import Store_Timezone, Report 
from pytz import timezone as pytz_timezone
from django.utils import timezone 

import datetime

stores = Store_Timezone.objects.all()[:50]
from StoreP_app.populate_data import trigger_report
report = Report.objects.create(status=Report.report_status.PENDING)
trigger_report(report)