from rest_framework import serializers
from location.models import Spot
from .models import Truck


class TruckSerializer(serializers.ModelSerializer):
    current_spot_zip = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Truck
        fields = ['unique_number', 'capacity', 'current_spot_zip']
        read_only_fields = ['unique_number', 'capacity']

    @staticmethod
    def get_current_spot_zip(obj):
        return obj.current_spot.zip_code


class TruckCreateSerializer(serializers.ModelSerializer):
    current_spot_zip = serializers.CharField(max_length=20, allow_blank=False, write_only=True)

    class Meta:
        model = Truck
        fields = ['unique_number', 'capacity', 'current_spot_zip']

    def create(self, validated_data):
        current_spot_zip = validated_data.pop('current_spot_zip')
        current_spot, _ = Spot.objects.get_or_create(zip_code=current_spot_zip)
        truck = Truck.objects.create(**validated_data, current_spot=current_spot)
        return truck


class TruckUpdateSerializer(serializers.ModelSerializer):
    current_spot_zip = serializers.CharField(max_length=20, allow_blank=False, write_only=True)

    class Meta:
        model = Truck
        fields = ['current_spot_zip']
        read_only_fields = ['unique_number', 'capacity']

    def update(self, instance, validated_data):
        current_spot_zip = validated_data.pop('current_spot_zip', None)
        if current_spot_zip:
            instance.current_spot, _ = Spot.objects.get_or_create(zip_code=current_spot_zip)
        instance.save()
        return instance
