from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


schema_view = get_schema_view(
        title="Social Network Documentation",
        description="Social Network API's with OpenAPI",
        version="1.0.0"
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/social_network/', include('social_network.urls')),
    path('api/get_token', jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    path('api/refresh_token', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title="Social Network Documentation"), name='docs'),
    path('openapi/', schema_view, name='openapi_schema'),
]
