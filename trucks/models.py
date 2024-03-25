from django.core.validators import MaxValueValidator
from django.db import models
from location.models import Spot


class Truck(models.Model):
    unique_number = models.CharField(max_length=5, unique=True)
    current_spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='trucks')
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(1000)],
                                           help_text="Capacity in kilograms."
                                           )

    def __str__(self):
        return f"Truck {self.unique_number} - Capacity: {self.capacity}kg"


