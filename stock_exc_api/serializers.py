from rest_framework import serializers
from stock_exc_api.models import StockExchangeIndex, Country, Historical_Data

#teste!!!

class StockExchangeIndexSerializer(serializers.ModelSerializer):	
	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name')

class StockExchangeIndexDetailSerializer(serializers.ModelSerializer):	
	country = serializers.SlugRelatedField(
		queryset = Country.objects.all(),
		slug_field = 'name',
		allow_null = True
		)

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'value', 'prev_close', 'change', 'change_percent', 'volume', 'country')


class CountrySerializer(serializers.ModelSerializer):	
	
	country = serializers.SlugRelatedField(
		queryset = Country.objects.all(),
		slug_field = 'name',
		allow_null = True
		)
	
	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'country')

class IndexCountry(serializers.ModelSerializer):
	country = CountrySerializer

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'country')

class HistDataSerializer(serializers.ModelSerializer):
	value = serializers.SlugRelatedField(
		queryset = Historical_Data.objects.all(),
		slug_field = 'value',
		allow_null = True
		)

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'value')


	