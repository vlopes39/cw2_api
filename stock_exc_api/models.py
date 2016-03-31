from django.db import models



class Country(models.Model):
	name = models.CharField(max_length=100, blank=True)


class StockExchangeIndex(models.Model):
	name = models.CharField(max_length=100, blank=True, default='')
	value = models.FloatField(null=True, blank=True)
	prev_close = models.FloatField(null=True, blank=True)
	change = models.FloatField(null=True, blank=True)
	change_percent = models.FloatField(null=True, blank=True)
	volume = models.FloatField(null=True, blank=True)
	country = models.ForeignKey(Country, null=True, blank=True)
	#hist_data = models.ForeignKey(Historical_Data, null=True, blank=True) #it should not be Foreign Key (many-to-one) - the right is one-to-many. Do the reverse in the other model
	#company = models.ForeignKey(Company, null=True, blank=True) #it should not be Foreign Key (many-to-one) - the right is one-to-many. Do the reverse in the other model



class Historical_Data(models.Model):
	index = models.ForeignKey(StockExchangeIndex, null=True, blank=True, related_name='hist_data') # many-to-one with Stock Exchange Index
	#date field
	hist_value = models.FloatField(null=True, blank=True)
	#open_price = models.FloatField(null=True, blank=True)
	high_price = models.FloatField(null=True, blank=True)
	low_price = models.FloatField(null=True, blank=True)
	volume = models.FloatField(null=True, blank=True)
	change_percent = models.FloatField(null=True, blank=True)

	class Meta:
		unique_together = ('index', 'hist_value')
		ordering = ['hist_value']


class Company(models.Model):
	name = models.CharField(max_length=100, blank=True)
	code = models.CharField(max_length=100, blank=True) 
	value = models.FloatField(null=True, blank=True) 
	prev_close = models.FloatField(null=True, blank=True) 
	change = models.FloatField(null=True, blank=True) 
	change_percent = models.FloatField(null=True, blank=True) 
	volume = models.FloatField(null=True, blank=True)
	country = models.ForeignKey(Country, null=True, blank=True) # Many-to-one with Country
	index = models.ForeignKey(StockExchangeIndex, null=True, blank=True, related_name='company') # many-to-one with Stock Exchange Index
	