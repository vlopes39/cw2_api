from rest_framework import serializers
from stock_exc_api.models import StockExchangeIndex, Country, Historical_Data

class CountrySerializer(serializers.ModelSerializer):	
	class Meta:
		model = Country
		fields = ('id', 'name')

class StockExchangeIndexSerializer(serializers.ModelSerializer):
	country = CountrySerializer	
	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'country')

	def create(seld, validate_data):
		country_data = validate_data.pop('country')
		index = StockExchangeIndex.objects.create(**validate_data)
		Country.objects.create(index=index, **country_data)

		return index

class StockExchangeIndexDetailSerializer(serializers.ModelSerializer):	
	country = CountrySerializer

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'value', 'prev_close', 'change', 'change_percent', 'volume', 'country')



class IndexCountry(serializers.ModelSerializer):
	country = CountrySerializer

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'country')
		'''
	def update(self, instance, validate_data):
		country_data = validate_data.pop('country')
		nation = instance.country

		nation.name = country_data.get('name', nation.name)
		nation.save()

		return instance
'''
		


class HistDataSerializer(serializers.ModelSerializer):
	
	index = serializers.SlugRelatedField(
		queryset = Historical_Data.objects.all(),
		slug_field = 'value',
		many = True		
		)
	
	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'index')


	