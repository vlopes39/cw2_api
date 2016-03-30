from rest_framework import serializers
from stock_exc_api.models import StockExchangeIndex, Country, Historical_Data, Company
#from django_extensions.db.fields import UUIDField

class CountrySerializer(serializers.ModelSerializer):	
	class Meta:
		model = Country
		fields = ('id', 'name')

class HistDataSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Historical_Data
		fields = ('id', 'hist_value', 'high_price')

class CompanySerializer(serializers.ModelSerializer):
	country = CountrySerializer(required=False)
	class Meta:
		model = Company
		fields = ('id', 'name', 'country')

class StockExchangeIndexSerializer(serializers.ModelSerializer):
	country = CountrySerializer(required=False)
	hist_data = HistDataSerializer(many=True, required=False)
	company = CompanySerializer(many=True, required=False)

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'country', 'hist_data', 'company')

	def create(self, validated_data):
		countries_data = validated_data.pop('country') # dados novos referentes ao country
		hist_datas_data = validated_data.pop('hist_data') # dados novos referentes ao Historical Data
		companies_data = validated_data.pop('company')

		country = Country.objects.create(**countries_data) # crio um objeto Country com os dados novos				
		index = StockExchangeIndex.objects.create(country=country, **validated_data) # crio um objeto Index com os dados novos (validated_data) e associo com o objeto Country

		#index = StockExchangeIndex.objects.create(**validated_data)
		for hist_data_data in hist_datas_data:
			Historical_Data.objects.create(index=index, **hist_data_data)

		for company_data in companies_data:
			Company.objects.create(index=index, **company_data)

		return index
    	

class StockExchangeIndexDetailSerializer(serializers.ModelSerializer):	
	country = CountrySerializer(required=False, many=False)
	hist_data = HistDataSerializer(many=True, required=False)
	company = CompanySerializer(many=True, required=False)

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'country', 'hist_data', 'company')

	def update(self, instance, validated_data):
		countries_data = validated_data.pop('country') # dados novos referentes ao country
		hist_datas_data = validated_data.pop('hist_data') # dados novos referentes ao Historical Data
		companies_data = validated_data.pop('company') # dados novos referentes a Company

		country = instance.country
		hist_data = instance.hist_data.all()
		company = instance.company.all()		

		instance.name = validated_data.get('name', instance.name)
		instance.save()

		for i in range(len(hist_data)):
			hist_data[i].hist_value = hist_datas_data[i].get('hist_value', hist_data[i].hist_value)
			hist_data[i].high_price = hist_datas_data[i].get('high_price', hist_data[i].high_price)
			hist_data[i].save()

		for j in range(len(company)):
			company[j].name = companies_data[j].get('name', company[j].name)
			company[j].save()

		country.name = countries_data.get('name', country.name)
		country.save()

		return instance

class CountryDetailSerializer(serializers.ModelSerializer):
	country = CountrySerializer(many=False)

	class Meta:
		model = StockExchangeIndex
		fields = ('id', 'name', 'country')

class HistDataDetailSerializer(serializers.ModelSerializer):
	hist_data = HistDataSerializer(many=True, required=False)
	#hist_data = serializers.PrimaryKeyRelatedField(
		#many=True,
		#required=False,
		#queryset=Historical_Data.objects.all(),
		#pk_field=UUIDField(format='hex')
		#)

	class Meta:
		model = StockExchangeIndex
		fields = ('hist_data',)

	'''
	def create(self, validated_data):
		hist_datas_data = validated_data.pop('hist_data') # dados novos referentes ao Historical Data
				
		#name = validated_data.pop('name') # crio um objeto Index com os dados novos (validated_data) e associo com o objeto Country

		#index = StockExchangeIndex.objects.create(**validated_data)

		index = StockExchangeIndex.objects.all().filter(pk=24)
		
		for hist_data_data in hist_datas_data:
			Historical_Data.objects.create(index=,**hist_data_data)
		
		return index
	'''










		




	