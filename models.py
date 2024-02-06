from django.contrib.auth.models import User
from django.db import models


# Location
class Site(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sites')
    registration_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=31)
    is_active = models.BooleanField(default=True)
    details = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    class Meta:
        verbose_name_plural = 'addresses'

    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=31)
    street_number = models.CharField(max_length=7, blank=True, null=True)
    city = models.CharField(max_length=31)
    province = models.CharField(max_length=7)
    region = models.CharField(max_length=31, blank=True, null=True)
    country = models.CharField(max_length=31)
    postal_code = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    details = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        return f"{self.street} {self.street_number}, {self.city} ({self.province}), {self.region}, {self.country}, {self.postal_code}"


# Devices
class Device(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=6)
    details = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        return self.id


class Server(Device):
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, related_name='servers')
    CHOISES = (
        ('RASPBERRY_PI_3', 'Raspberry_Pi_3'),
        ('RASPBERRY_PI_4', 'Raspberry_Pi_4'),
        ('TOCS_SERVER', 'Tocs_Server'),
    )
    model = models.CharField(max_length=31, choices=CHOISES)


class LocalWeatherStation(Device):
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, related_name='local_weather_station')
    CHOISES = (
        ('SIR_Toscana', 'SIR_Toscana'),
    )
    model = models.CharField(max_length=31, choices=CHOISES)


class WeatherStation(Device):
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, related_name='weather_stations')
    CHOISES = (
        ('Davis', 'Davis'),
    )
    model = models.CharField(max_length=31, choices=CHOISES)


class SoilStation(Device):
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, related_name='soil_stations')
    CHOISES = (
        ('TMS_Lolly', 'TMS_Lolly'),
    )
    model = models.CharField(max_length=31, choices=CHOISES)


class Tocs(Device):
    mac = models.CharField(max_length=18, primary_key=True)
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, related_name='tocs')

    def __str__(self):
        return self.mac


# Data
# un evento è un CSV
# CSV Che hanno duration<1 min non vanno scaricati
class TocsEvent(models.Model):
    id = models.AutoField(primary_key=True)
    tocs = models.ForeignKey(
        Tocs, on_delete=models.CASCADE, related_name='events')
    csv_path = models.FilePathField()
    start = models.DateTimeField()
    duration = models.DateTimeField()
    ax_mean = models.FloatField()
    ay_mean = models.FloatField()
    az_mean = models.FloatField()
    ax_std = models.FloatField()
    ay_std = models.FloatField()
    az_std = models.FloatField()
    ax_peak = models.FloatField()
    ay_peak = models.FloatField()
    az_peak = models.FloatField()

    def __str__(self):
        return self.id


# Note the row is filled with resampled data
# Use linear interpolation to resample
# Check MADE code
class TocsCSVRow(models.Model):
    id = models.AutoField(primary_key=True)
    events = models.ForeignKey(
        TocsEvent, on_delete=models.CASCADE, related_name='csv_rows')
    time = models.DateTimeField()
    ax = models.FloatField()
    ay = models.FloatField()
    az = models.FloatField()
    temp = models.FloatField()

    def __str__(self):
        return self.id
