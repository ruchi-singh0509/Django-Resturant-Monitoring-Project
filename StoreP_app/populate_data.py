import tempfile
from .models import (
    Store_status,
    Store_Timezone,
    report_status,
    Report,
)
from django.utils import timezone
from pytz import timezone as pytz_timezone
from datetime import datetime
import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StoreProject.settings")


def trigger_report(report):
    csv_data = []

    # Only triggering report for the first 200 resturants
    restros = Store_Timezone.objects.all()[:200]
    for restro in restros:
        print(restro)
        data = generate_report(restro)
        csv_data.append(data)
    generate_csv_file(report, csv_data)
    return report


def generate_report(restro):
    # Get the resturant's timezone
    store_tzone = restro.timezone_str or "America/Chicago"
    target_timezone = pytz_timezone(store_tzone)

    time = Store_status.objects.all().order_by("-timestamp").first().timestamp
    local_time = time.astimezone(target_timezone)
    utc_timezone = pytz_timezone("UTC")
    utc_time = time.astimezone(utc_timezone)
    current_day = local_time.weekday()
    current_time = local_time.time()
    # Get the last one hour data
    last_one_hour_data = get_last_one_hour_data(
        restro, utc_time, current_day, current_time
    )

    # Get the last one day data
    last_one_day_data = get_last_one_day_data(
        restro, utc_time, current_day, current_time
    )

    # Get the last one week data
    last_one_week_data = get_last_one_week_data(
        restro, utc_time, current_day, current_time
    )

    data = []
    data.append(restro.pk)
    data.extend(list(last_one_hour_data.values()))
    data.extend(list(last_one_day_data.values()))
    data.extend(list(last_one_week_data.values()))

    return data


def generate_csv_file(report, csv_data):
    with tempfile.TemporaryDirectory() as temp_direc:
        file_name = f"{report.pk}.csv"
        temp_file_path = os.path.join(temp_direc, file_name)

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
        Report.status = report_status.COMPLETED
        report.save()


def get_last_one_hour_data(restro, utc_time, current_day, current_time):
    last_one_hour_data = {"uptime": 0, "downtime": 0, "unit": "minutes"}

    # Check if the resturant is open in the last one hour
    resturant_is_open = restro.timmings.filter(
        day=current_day, start_time_lte=current_time, end_time_gte=current_time
    ).exists()
    if not resturant_is_open:
        return last_one_hour_data

    # Get the latest status within the last one hour
    last_one_hour_log = restro.restro_status.filter(
        timestamp_gte=utc_time - datetime.timedelta(hours=1)
    ).order_by("timestamp")
    if last_one_hour_log:
        last_one_hour_log_status = last_one_hour_log[0].status
        if last_one_hour_log_status == Store_status.ACTIVE:
            last_one_hour_data["uptime"] = 60
        else:
            last_one_hour_data["downtime"] = 60

    return last_one_hour_data


def get_last_one_day_data(restro, utc_time, current_day, current_time):
    last_one_day_data = {"uptime": 0, "downtime": 0, "unit": "hours"}
    one_day_ago = (current_day - 1) if current_day > 0 else 6
    # checking if resturant is open in last one day
    resturant_is_open = restro.timmings.filter(
        day_gte=one_day_ago,
        day_lte=current_day,
        start_time_lte=current_time,
        end_time_gte=current_time,
    ).exists()
    if not resturant_is_open:
        return last_one_day_data
    # getting all the logs in last one day
    last_one_day_log = restro.restro_status.filter(
        timestamp_gte=utc_time - datetime.timedelta(days=1)
    ).order_by("timestamp")
    for log in last_one_day_log:
        # checkig if log is in store business hours
        log_in_store_business_hours = restro.timmings.filter(
            dayOfWeek=log.timestamp.weekday(),
            start_time_lte=log.timestamp.time(),
            end_time_gte=log.timestamp.time(),
        ).exists()
        # checking if log is in store business hours and status is active
        if not log_in_store_business_hours:
            continue
        if log.status == Store_status.ACTIVE:
            last_one_day_data["uptime"] += 1
        else:
            last_one_day_data["downtime"] += 1
    return last_one_day_data


def get_last_one_week_data(restro, utc_time, current_day, current_time):
    last_one_week_data = {"uptime": 0, "downtime": 0, "unit": "hours"}
    one_week_ago = (current_day - 7) if current_day > 0 else 0
    # checking if resturant is open in last one week
    resturant_is_open = restro.timmings.filter(
        day_gte=one_week_ago,
        day_lte=current_day,
        start_time_lte=current_time,
        end_time_gte=current_time,
    ).exists()
    if not resturant_is_open:
        return last_one_week_data
    # getting all the logs in last one week
    last_one_week_log = restro.restro_status.filter(
        timestamp_gte=utc_time - datetime.timedelta(days=7)
    ).order_by("timestamp")
    for log in last_one_week_log:
        # checking if log is in business hours
        log_in_store_business_hours = restro.timmings.filter(
            day=log.timestamp.weekday(),
            start_time_lte=log.timestamp.time(),
            end_time_gte=log.timestamp.time(),
        ).exists()
        # checking if log is in business hours and status is active
        if not log_in_store_business_hours:
            continue
        if log.status == Store_status.ACTIVE:
            last_one_week_data["uptime"] += 1
        else:
            last_one_week_data["downtime"] += 1

    return last_one_week_data
