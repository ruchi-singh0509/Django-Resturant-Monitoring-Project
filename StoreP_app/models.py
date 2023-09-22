from datetime import timezone
from django.utils import timezone
from django.db import models


# Create your models here.


class Store_Timezone(models.Model):
    store_id = models.CharField(max_length=50, primary_key=True, default=None)
    timezone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.store_id


class Days(models.IntegerChoices):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


class Store_Business_Hour(models.Model):
    store = models.ForeignKey(
        Store_Timezone,
        on_delete=models.CASCADE,
        default=None,
        related_name="store_hour",
    )
    dayOfWeek = models.IntegerField(choices=Days.choices)
    start_time = models.TimeField(default="")
    end_time = models.TimeField(default="")

    def __str__(self) -> str:
        return f"{self.store.store_id},{self.start_time},{self.end_time}"


class Store_status(models.Model):
    store = models.ForeignKey(
        Store_Timezone,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="status_store",
    )
    status = models.CharField(
        choices=[("active", "Active"), ("inactive", "Inactive")], max_length=25
    )
    timestamp = models.DateTimeField(
        verbose_name="Time Stamp in UTC", null=True, blank=True
    )

    def local_timestamp(self):
        return self.timestamp.astimezone(self.store.timezone)

    def __str__(self) -> str:
        return f"{self.store.store_id},{self.status},{self.timestamp}"


class Report(models.Model):
    store = models.ForeignKey(
        Store_Timezone,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="report_store",
    )
    report_status = models.CharField(
        choices=[("pending", "Pending"), ("completed", "Completed")],
        max_length=50,
        default="Pending",
    )
    report_url = models.FileField(upload_to="reports", null=True, blank=True)
