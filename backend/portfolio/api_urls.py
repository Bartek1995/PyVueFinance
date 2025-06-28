from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, StockPriceViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'stock-prices', StockPriceViewSet)

urlpatterns = router.urls
