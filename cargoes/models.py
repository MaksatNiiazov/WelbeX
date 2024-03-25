from django.core.validators import MaxValueValidator
from django.db import models

from location.models import Spot


class Cargo(models.Model):
    pick_up_spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='cargo_pick_ups',
                                     verbose_name="Pick-up Location")
    delivery_spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='cargo_deliveries',
                                      verbose_name="Delivery Location")
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(1000)],
                                         help_text="Weight of the cargo in kilograms."
                                         )
    description = models.TextField(blank=True, null=True, help_text="Description of the cargo.")

    def __str__(self):
        return f"Cargo from {self.pick_up_spot} to {self.delivery_spot} - {self.weight}kg"
