
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


    path('step-1/', TemplateView.as_view(template_name='accounts/register_step_1.html'), name='register_step_1'),
    path('step-2/', TemplateView.as_view(template_name='accounts/register_step_2.html'), name='register_step_2'),
    path('step-3/', TemplateView.as_view(template_name='accounts/register_step_3.html'), name='register_step_3'),
    path('', TemplateView.as_view(template_name='build/home_page.html'), name='home_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('orders/', include('orders.urls')),
]
