from rest_framework import serializers
from cargoes.models import Cargo
from location.models import Spot


class CargoSerializer(serializers.ModelSerializer):
    pick_up_zip = serializers.SerializerMethodField(read_only=True)
    delivery_zip = serializers.SerializerMethodField(read_only=True)
    trucks_in_range = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['pick_up_zip', 'delivery_zip', 'weight', 'description', 'trucks_in_range']

    @staticmethod
    def get_pick_up_zip(obj):
        return obj.pick_up_spot.zip_code

    @staticmethod
    def get_delivery_zip(obj):
        return obj.delivery_spot.zip_code

    @staticmethod
    def get_trucks_in_range(obj):
        return getattr(obj, 'trucks_in_range', [])


class CargoCreateSerializer(serializers.ModelSerializer):
    pick_up_zip = serializers.CharField(max_length=20, write_only=True)
    delivery_zip = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Cargo
        fields = ['pick_up_zip', 'delivery_zip', 'weight', 'description']

    def create(self, validated_data):
        pick_up_zip = validated_data.pop('pick_up_zip')
        delivery_zip = validated_data.pop('delivery_zip')
        pick_up_spot = Spot.objects.get_or_create(zip_code=pick_up_zip)[0]
        delivery_spot = Spot.objects.get_or_create(zip_code=delivery_zip)[0]
        return Cargo.objects.create(pick_up_spot=pick_up_spot, delivery_spot=delivery_spot, **validated_data)


class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['weight', 'description']

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance