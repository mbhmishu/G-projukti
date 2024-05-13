from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Projukti coding test",
        default_version='v1',
        description="""Md Belal Hossain
        Django Backend Developer""",
        terms_of_service="https://www.gprojukti.com/about-us",
        contact=openapi.Contact(email="mbhmishu@gmail.com",),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user_auth.urls')),
    path('api/v1/product/', include('product_discount_app.urls')),
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)