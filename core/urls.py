from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views


schema_view = get_schema_view(
   openapi.Info(
      title="Social Network API's swagger Documentation",
      default_version='v1',
      description="Social Network description",
      terms_of_service="https://www.socialnetwork.com/policies/terms/",
      contact=openapi.Contact(email="socialnetwork@company.com"),
      license=openapi.License(name="Social Network License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('social_network/', include('social_network.urls')),
    path('get_token/', jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token/', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
