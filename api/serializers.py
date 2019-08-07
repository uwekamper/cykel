from rest_framework import routers, serializers, viewsets

from bikesharing.models import Bike
from bikesharing.models import Lock
from bikesharing.models import Station

#class LocationSerializer(serializers.HyperlinkedModelSerializer):
#	class Meta:


# Serializers define the API representation.
class LockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lock
        fields = ('mac_address',)

# Serializers define the API representation.
class BikeSerializer(serializers.HyperlinkedModelSerializer):
    lock = LockSerializer()

    class Meta:
        model = Bike
        fields = ('bike_number', 'lock', 'current_position',)

class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ('station_name','location', 'max_bikes', 'status')

class GbfsFreeBikeStatusSerialzer(serializers.HyperlinkedModelSerializer):
	bike_id = serializers.CharField(source='bike_number', read_only=True)

	class Meta:
		model = Bike
		fields = ('bike_id', )

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['is_reserved'] = False #Default to False TODO: maybe configuration later
		representation['is_disabled'] = False #Default to False TODO: maybe configuration later
		if (instance.current_position.x and instance.current_position.y):
			representation['lat'] = instance.current_position.y
			representation['lon'] = instance.current_position.x
		return representation

class GbfsStationInformationSerialzer(serializers.HyperlinkedModelSerializer):
	name = serializers.CharField(source='station_name', read_only=True)
	capacity = serializers.IntegerField(source='max_bikes', read_only=True)
	id = serializers.CharField(read_only=True)

	class Meta:
		model = Station
		fields = ('name', 'capacity', 'id', )
	def to_representation(self, instance):
		print (dir(instance))
		representation = super().to_representation(instance)
		#representation['is_reserved'] = False #Default to False TODO: maybe configuration later
		#representation['is_disabled'] = False #Default to False TODO: maybe configuration later
		if (instance.location.x and instance.location.y):
			representation['lat'] = instance.location.y
			representation['lon'] = instance.location.x
		return representation