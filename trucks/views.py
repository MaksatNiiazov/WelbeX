from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from location.models import Spot
from .models import Truck
from .serializers import TruckSerializer, TruckUpdateSerializer, TruckCreateSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def get_serializer_class(self):
        if self.action in ['create']:
            return TruckCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TruckUpdateSerializer
        return TruckSerializer

    def create(self, request, *args, **kwargs):
        current_spot = request.data.get('current_spot_zip_write')
        try:
            current_spot = Spot.objects.get(zip_code=current_spot)
        except Spot.DoesNotExist:
            raise ValidationError('ZIP codes is invalid.')

        truck_data = request.data.copy()
        truck_data['current_spot'] = current_spot.id

        serializer = self.get_serializer(data=truck_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        truck = self.get_object()
        current_spot_zip = request.data.get('current_spot_zip')

        if current_spot_zip:
            try:
                current_spot = Spot.objects.get(zip_code=current_spot_zip)
            except Spot.DoesNotExist:
                raise ValidationError('ZIP code is invalid.')

            request.data['current_spot'] = current_spot.id

        serializer = self.get_serializer(truck, data=request.data, partial=kwargs.pop('partial', True))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
