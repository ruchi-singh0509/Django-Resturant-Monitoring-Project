import django

django.setup()
from datetime import datetime
import tempfile
import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StoreProject.settings")
from .models import Store_status, Store_Timezone, Report
from django.utils import timezone
from pytz import timezone as pytz_timezone


def trigger_report(report):
    csv_data = []

    # Only triggering report for the first 400 stores
    stores = Store_Timezone.objects.all()[:400]
    for store in stores:
        print(store)
        store_instance = Store_Timezone.objects.get(store)
        data = generate_report(store_instance)
        csv_data.append(data)
    generate_csv_file(report, csv_data)
    return report


def generate_report(store):
    # Get the store's timezone
    store_tzone = store.timezone or "America/Chicago"
    target_timezone = pytz_timezone(store_tzone)

    time = Store_status.objects.all().order_by("-timestamp").first().timestamp
    local_time = time.astimezone(target_timezone)
    utc_timezone = pytz_timezone("UTC")
    utc_time = time.astimezone(utc_timezone)
    current_day = local_time.weekday()
    current_time = local_time.time()
    # Get the last one hour data
    last_one_hour_data = get_last_one_hour_data(
        store, utc_time, current_day, current_time
    )

    # Get the last one day data
    last_one_day_data = get_last_one_day_data(
        store, utc_time, current_day, current_time
    )

    # Get the last one week data
    last_one_week_data = get_last_one_week_data(
        store, utc_time, current_day, current_time
    )

    data = []
    data.extend(list(last_one_hour_data.values()))
    data.extend(list(last_one_day_data.values()))
    data.extend(list(last_one_week_data.values()))

    return data


def generate_csv_file(report, csv_data):
    with tempfile.TemporaryDirectory() as t_direc:
        file_name = f"{report.pk}.csv"
        temp_file_path = os.path.join(t_direc, file_name)

        with open(temp_file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                [
                    "store_id",
                    "last_one_hour_uptime",
                    "last_one_hour_downtime",
                    "last_one_hour_unit",
                    "last_one_day_uptime",
                    "last_one_day_downtime",
                    "last_one_day_unit",
                    "last_one_week_uptime",
                    "last_one_week_downtime",
                    "last_one_week_unit",
                ]
            )
            for data in csv_data:
                csv_writer.writerow(data)

        # Save the CSV file as a report URL
        Report.report_url.save(file_name, open(temp_file_path, "rb"))
        Report.report_status = "completed"
        report.save()


def get_last_one_hour_data(store, utc_time, current_day, current_time):
    last_one_hour_data = {"uptime": 0, "downtime": 0, "unit": "minutes"}

    # Check if the store is open in the last one hour
    is_store_open = store.timings.filter(
        day=current_day, start_time__=current_time, end_time__=current_time
    ).exists()
    if not is_store_open:
        return last_one_hour_data

    # Get the latest status within the last one hour
    last_one_hour_log = store.status_logs.filter(
        timestamp__=utc_time - datetime.timedelta(hours=1)
    ).order_by("timestamp")
    if last_one_hour_log:
        last_one_hour_log_status = last_one_hour_log[0].status
        if last_one_hour_log_status == Store_status.ACTIVE:
            last_one_hour_data["uptime"] = 60
        else:
            last_one_hour_data["downtime"] = 60

    return last_one_hour_data


def get_last_one_day_data(store, utc_time, current_day, current_time):
    last_one_day_data = {"uptime": 0, "downtime": 0, "unit": "hours"}
    one_day_ago = (current_day - 1) % 7 if current_day > 0 else 6
    # checking if store is open in last one day
    is_store_open = store.timings.filter(
        day__gte=one_day_ago,
        day__lte=current_day,
        start_time__lte=current_time,
        end_time__gte=current_time,
    ).exists()
    if not is_store_open:
        return last_one_day_data
    # getting all the logs in last one day
    last_one_day_logs = store.status_logs.filter(
        timestamp__gte=utc_time - timezone.timedelta(days=1)
    ).order_by("timestamp")
    for log in last_one_day_logs:
        # checkig if log is in store business hours
        log_in_store_business_hours = store.timings.filter(
            dayOfWeek=log.timestamp.weekday(),
            start_time__lte=log.timestamp.time(),
            end_time__gte=log.timestamp.time(),
        ).exists()
        # checking if log is in store business hours and status is active
        if not log_in_store_business_hours:
            continue
        if log.status == Store_status.ACTIVE:
            last_one_day_data["uptime"] += 1
        else:
            last_one_day_data["downtime"] += 1
    return last_one_day_data


def get_last_one_week_data(store, utc_time, current_day, current_time):
    last_one_week_data = {"uptime": 0, "downtime": 0, "unit": "hours"}
    one_week_ago = (current_day - 7) % 7 if current_day > 0 else 0
    # checking if store is open in last one week
    is_store_open = store.timings.filter(
        day__gte=one_week_ago,
        day__lte=current_day,
        start_time__lte=current_time,
        end_time__gte=current_time,
    ).exists()
    if not is_store_open:
        return last_one_week_data
    # getting all the logs in last one week
    last_one_week_logs = store.status_logs.filter(
        timestamp__gte=utc_time - timezone.timedelta(days=7)
    ).order_by("timestamp")
    for log in last_one_week_logs:
        # checking if log is in business hours
        log_in_store_business_hours = store.timings.filter(
            day=log.timestamp.weekday(),
            start_time__lte=log.timestamp.time(),
            end_time__gte=log.timestamp.time(),
        ).exists()
        # checking if log is in business hours and status is active
        if not log_in_store_business_hours:
            continue
        if log.status == Store_status.ACTIVE:
            last_one_week_data["uptime"] += 1
        else:
            last_one_week_data["downtime"] += 1

    return last_one_week_data
