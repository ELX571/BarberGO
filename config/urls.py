
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
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

    path('chat/', include('chat.urls')),
    
    # Frontend Routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('create-post/', TemplateView.as_view(template_name='create_post.html'), name='create-post'),
    path('orders-ui/', TemplateView.as_view(template_name='orders.html'), name='orders-ui'),
    path('notifications/', TemplateView.as_view(template_name='notifications.html'), name='notifications'),
    path('filters/', TemplateView.as_view(template_name='filters.html'), name='filters'),
    path('hairstyles/', TemplateView.as_view(template_name='hairstyles.html'), name='hairstyles'),
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
