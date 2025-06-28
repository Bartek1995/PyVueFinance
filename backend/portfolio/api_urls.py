from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, FetchCompanyData, StockPriceViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'stock-prices', StockPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('fetch-company-data/', FetchCompanyData.as_view(), name='fetch-company-data'),
]
