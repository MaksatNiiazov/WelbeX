from geopy.distance import geodesic
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from location.models import Spot
from trucks.models import Truck
from .models import Cargo
from .serializers import CargoSerializer, CargoCreateSerializer, CargoUpdateSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CargoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CargoUpdateSerializer
        return CargoSerializer

    def list(self, request, *args, **kwargs):
        cargoes = Cargo.objects.all()
        for cargo in cargoes:
            cargo_trucks = []
            trucks = Truck.objects.all()
            for truck in trucks:
                cargo_location = (cargo.pick_up_spot.latitude, cargo.pick_up_spot.longitude)
                truck_location = (truck.current_spot.latitude, truck.current_spot.longitude)
                distance = geodesic(cargo_location, truck_location).miles
                if distance <= 450:
                    cargo_trucks.append(truck.unique_number)
            cargo.trucks_in_range = cargo_trucks
        serializer = self.get_serializer(cargoes, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pick_up_zip = request.data.get('pick_up_zip')
        delivery_zip = request.data.get('delivery_zip')
        try:
            pick_up_spot = Spot.objects.get(zip_code=pick_up_zip)
            delivery_spot = Spot.objects.get(zip_code=delivery_zip)
        except Spot.DoesNotExist:
            raise ValidationError('One of the ZIP codes is invalid.')

        cargo_data = request.data.copy()
        cargo_data['pick_up_spot'] = pick_up_spot.id
        cargo_data['delivery_spot'] = delivery_spot.id

        serializer = self.get_serializer(data=cargo_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        cargo = self.get_object()
        cargo_data = self.get_serializer(cargo).data
        trucks_in_range = 0
        appropriate_trucks = 0
        trucks_info = []
        cargo_location = (cargo.pick_up_spot.latitude, cargo.pick_up_spot.longitude)

        for truck in Truck.objects.all():
            truck_location = (truck.current_spot.latitude, truck.current_spot.longitude)
            distance = geodesic(cargo_location, truck_location).miles
            if distance <= 450:
                trucks_in_range += 1
                if truck.capacity >= cargo.weight:
                    appropriate_trucks += 1

            trucks_info.append({
                'truck_number': truck.unique_number,
                'distance_miles': distance,
                'capacity': truck.capacity,
                'truck_in_range': True if distance <= 450 else False,
                'permissible_capacity': True if cargo.weight <= truck.capacity else False
            })
        cargo_data['appropriate_trucks'] = appropriate_trucks
        cargo_data['trucks_in_range'] = trucks_in_range
        cargo_data['trucks_info'] = trucks_info

        return Response(cargo_data)

    def update(self, request, *args, **kwargs):
        cargo = self.get_object()

        update_data = {
            'weight': request.data.get('weight'),
            'description': request.data.get('description')
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            raise ValidationError("No valid field(s) to update.")

        serializer = CargoUpdateSerializer(cargo, data=update_data, partial=kwargs.pop('partial', True))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)