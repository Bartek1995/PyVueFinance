from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CompanyViewSet, StockPriceViewSet,
    FetchCompanyData, CompanyDetailView, CompanyPriceHistory
)

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"stock-prices", StockPriceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("fetch-company-data/", FetchCompanyData.as_view(), name="fetch-company-data"),
    path('company/<str:ticker>/', CompanyDetailView.as_view()),
    path('company/<str:ticker>/prices/', CompanyPriceHistory.as_view()),
]
