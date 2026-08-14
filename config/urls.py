
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view=get_schema_view(
    openapi.Info(
        title="BarberGo API",
        default_version='v1',
        description="BarberGo API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('orders/', include('orders.urls')),
    
    # Frontend Routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('create-post/', TemplateView.as_view(template_name='create_post.html'), name='create-post'),
    path('orders-ui/', TemplateView.as_view(template_name='orders.html'), name='orders-ui'),
    path('notifications/', TemplateView.as_view(template_name='notifications.html'), name='notifications'),
]
