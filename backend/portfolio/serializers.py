from rest_framework import serializers
from .models import Company, StockPrice

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class StockPriceSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='ticker', queryset=Company.objects.all())
    class Meta:
        model = StockPrice
        fields = '__all__'
