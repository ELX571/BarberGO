from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register('auth-jwt',views.AuthApiViewSet,basename='auth-jwt')
router.register('forget-password',views.VerificationCodeViewSet,basename='forget-password')

urlpatterns = router.urls
