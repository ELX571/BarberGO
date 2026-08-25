from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register('posts',views.Posts,basename='posts')
router.register('recommended-posts', views.RecommendedPostViewSet, basename='recommended-posts')

urlpatterns = [

]+ router.urls
