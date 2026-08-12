from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register('posts',views.Posts,basename='posts')

urlpatterns = [

]+ router.urls