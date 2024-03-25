from django.db import transaction
import random

from cargoes.models import Cargo
from cargoes.utils.cargo_names import get_cargo_names
from location.models import Spot


def create_random_cargoes(number_of_cargoes=100):
    existing_cargoes_count = Cargo.objects.count()
    cargoes_to_create = number_of_cargoes - existing_cargoes_count

    if cargoes_to_create <= 0:
        print("There are already enough cargoes in the database.")
        return

    # Продолжаем создание новых грузов
    spots = list(Spot.objects.all())
    descriptions = get_cargo_names()

    if len(spots) < 2:
        print("Need at least 2 distinct spots to create cargoes.")
        return

    with transaction.atomic():
        for _ in range(cargoes_to_create):
            pick_up_spot, delivery_spot = random.sample(spots, 2)
            weight = random.randint(1, 1000)
            description = random.choice(descriptions)

            Cargo.objects.create(
                pick_up_spot=pick_up_spot,
                delivery_spot=delivery_spot,
                weight=weight,
                description=f"{description}, from {pick_up_spot.city.name} to {delivery_spot.city.name}"
            )

        print(f"{cargoes_to_create} cargoes have been created successfully.")