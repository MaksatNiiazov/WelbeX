from django.db.utils import IntegrityError
import random
import string
import logging

from location.models import Spot
from trucks.models import Truck

logger = logging.getLogger(__name__)


def create_initial_trucks():
        if Truck.objects.count() < 20:
            spot_ids = list(Spot.objects.values_list('id', flat=True))
            if not spot_ids:
                logger.error("No Spot objects found. Trucks will not be created.")
                return

            for _ in range(20 - Truck.objects.count()):
                unique_number = ''.join(random.choices(string.digits, k=4)) + random.choice(string.ascii_uppercase)
                random_spot_id = random.choice(spot_ids)
                try:
                    Truck.objects.create(
                        unique_number=unique_number,
                        current_spot_id=random_spot_id,
                        capacity=random.randint(1, 1000)
                    )
                except IntegrityError:
                    logger.error(f"Failed to create a truck with number {unique_number}. Integrity error.")
                    continue
        logger.info("Initial trucks creation process completed.")
