from rest_framework import routers

from orders.views import OrderViewSet

router = routers.DefaultRouter()
router.register('',OrderViewSet,basename='orders')
urlpatterns = [

] + router.urls