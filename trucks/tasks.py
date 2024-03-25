from celery import shared_task
from random import randint
from .models import Spot, Truck

@shared_task
def update_truck_locations():
    spots = list(Spot.objects.all())
    trucks = Truck.objects.all()
    for truck in trucks:
        random_spot = spots[randint(0, len(spots) - 1)]
        truck.current_spot = random_spot
        truck.save()
