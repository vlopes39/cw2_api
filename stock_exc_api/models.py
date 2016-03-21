from django.db import models


class Country(models.Model):
	name = models.CharField(max_length=100, blank=True, default="Brazil")

class StockExchangeIndex(models.Model):
	name = models.CharField(max_length=100, blank=True, default='')
	value = models.FloatField(null=True, blank=True)
	prev_close = models.FloatField(null=True, blank=True)
	change = models.FloatField(null=True, blank=True)
	change_percent = models.FloatField(null=True, blank=True)
	volume = models.FloatField(null=True, blank=True)
	country = models.ForeignKey(Country, null=True, blank=True, related_name='country')
	#hist_data = models.ForeignKey(Historical_Data, null=True, blank=True) #it should not be Foreign Key (many-to-one) - the right is one-to-many. Do the reverse in the other model
	#company = models.ForeignKey(Company, null=True, blank=True) #it should not be Foreign Key (many-to-one) - the right is one-to-many. Do the reverse in the other model



class Historical_Data(models.Model):
	#date field
	value = models.FloatField(null=True, blank=True, default='')
	#open_price = models.FloatField(null=True, blank=True)
	high_price = models.FloatField(null=True, blank=True, default=0.0)
	low_price = models.FloatField(null=True, blank=True, default=0.0)
	volume = models.FloatField(null=True, blank=True, default=0.0)
	change_percent = models.FloatField(null=True, blank=True, default=0.0)
	index = models.ForeignKey(StockExchangeIndex, null=True, blank=True, related_name='index') # many-to-one with Stock Exchange Index

class Company(models.Model):
	name = models.CharField(max_length=100, blank=True, default='')
	code = models.CharField(max_length=100, blank=True, default='')
	value = models.FloatField(null=True, blank=True)
	prev_close = models.FloatField(null=True, blank=True)
	change = models.FloatField(null=True, blank=True)
	change_percent = models.FloatField(null=True, blank=True)
	volume = models.FloatField(null=True, blank=True)
	country = models.ForeignKey(Country, null=True, blank=True) # Many-to-one with Country
	index = models.ForeignKey(StockExchangeIndex, null=True, blank=True) # many-to-one with Stock Exchange Index
