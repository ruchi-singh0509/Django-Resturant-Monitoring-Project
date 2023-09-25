from django.db import models


# Create your models here.


class Store_Timezone(models.Model):
    store_id = models.CharField(max_length=50, primary_key=True, default=None)
    timezone_str = models.CharField(max_length=50, null=True, blank=True)

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
    restro = models.ForeignKey(
        Store_Timezone,
        on_delete=models.CASCADE,
        default=None,
        related_name="timmings",
    )
    dayOfWeek = models.IntegerField(choices=Days.choices)
    start_time = models.TimeField(default="")
    end_time = models.TimeField(default="")

    def __str__(self) -> str:
        return f"{self.restro.store_id},{self.start_time},{self.end_time}"


class store_status(models.IntegerChoices):
    INACTIVEACTIVE = 0
    ACTIVE = 1


class Store_status(models.Model):
    restro = models.ForeignKey(
        Store_Timezone,
        on_delete=models.CASCADE,
        related_name="restro_status",
        default=None,
    )
    status = models.IntegerField(choices=store_status.choices, default=None)
    timestamp = models.DateTimeField(
        verbose_name="Time Stamp in UTC", null=True, blank=True
    )

    def local_timestamp(self):
        return self.timestamp.astimezone(self.restro.timezone_str)

    def __str__(self) -> str:
        return f"{self.restro.store_id},{self.status},{self.timestamp}"


class report_status(models.IntegerChoices):
    PENDING = 0
    COMPLETED = 1


class Report(models.Model):
    restro = models.ForeignKey(
        Store_Timezone,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
        default=None,
    )
    status = models.IntegerField(choices=report_status.choices, default=None)
    report_url = models.FileField(upload_to="reports", null=True, blank=True)
