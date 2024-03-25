from django.core.management.base import BaseCommand
import csv
from django.db import transaction

from cargoes.utils.create_cargoes import create_random_cargoes
from trucks.utils.create_trucks import create_initial_trucks
from location.models import City, Spot, State, County, LocationDetail

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        print('Imports data from a CSV file into the database begun.')

        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            states_to_create = []
            counties_to_create = []
            cities_to_create = []
            spots_to_create = []
            location_details_to_create = []

            for row in reader:
                state = State(
                    state_id=row['state_id'],
                    name=row['state_name']
                )
                states_to_create.append(state)

                county = County(
                    state=state,
                    fips=row['county_fips'],
                    name=row['county_name'],
                    county_fips_all=row['county_fips_all'],
                    county_names_all=row['county_names_all'],
                    population=row['population'] if row['population'] else 0,
                    county_weights=row['county_weights']
                )
                counties_to_create.append(county)

                city = City(
                    county=county,
                    name=row['city'],
                    zcta=row['zcta'] == 'ИСТИНА',
                    parent_zcta=row['parent_zcta'] if row['parent_zcta'] else None,
                    timezone=row['timezone']
                )
                cities_to_create.append(city)

                spot = Spot(
                    city=city,
                    description=f"{row['city']} {row['zip']}",
                    zip_code=row['zip'],
                    latitude=float(row['lat']),
                    longitude=float(row['lng'])
                )
                spots_to_create.append(spot)

                location_detail = LocationDetail(
                    spot=spot,
                    population=int(row['population']) if row['population'] else 0,
                    density=float(row['density']) if row['density'] else 0.0,
                    county_weights=row['county_weights'],
                    imprecise=row['imprecise'] == 'ЛОЖЬ',
                    military=row['military'] == 'ЛОЖЬ'
                )
                location_details_to_create.append(location_detail)

            State.objects.bulk_create(states_to_create)
            County.objects.bulk_create(counties_to_create)
            City.objects.bulk_create(cities_to_create)
            Spot.objects.bulk_create(spots_to_create)
            LocationDetail.objects.bulk_create(location_details_to_create)

        create_initial_trucks()
        create_random_cargoes()
        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV.'))
