from django.db import models
from django.db.models import JSONField


class State(models.Model):
    state_id = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.state_id})"


class County(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='counties')
    fips = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    county_fips_all = models.CharField(max_length=255, blank=True, null=True)
    county_names_all = models.CharField(max_length=255, blank=True, null=True)
    county_weights = models.JSONField(default=dict, help_text="Distribution of the city across counties.")
    population = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class City(models.Model):
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True, related_name='cities')
    name = models.CharField(max_length=255)
    zcta = models.BooleanField(default=False)
    parent_zcta = models.CharField(max_length=20, null=True, blank=True)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, "


class Spot(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='spots')
    description = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=20, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        description = f" - {self.description}" if self.description else ""
        return f"Spot in {self.city.name} {description} ({self.latitude}, {self.longitude}) ZIP {self.zip_code}"


class LocationDetail(models.Model):
    spot = models.OneToOneField(Spot, on_delete=models.CASCADE, primary_key=True, related_name='details')
    population = models.IntegerField(null=True, blank=True)
    density = models.FloatField(null=True, blank=True)
    county_weights = JSONField(blank=True, null=True)
    imprecise = models.BooleanField(default=False)
    military = models.BooleanField(default=False)

    def __str__(self):
        return f"Details for {self.spot}"
