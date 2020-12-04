from datetime import datetime
from django.contrib import admin
from django.urls import include,path
from django.contrib.auth.views import LoginView, LogoutView
from app import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Gografen API",
      default_version='v1',
      description="Docs",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@snippets.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('user/<int:pk>/',views.appUserView.as_view({'get':'retrieve','put':'update'})),
   path('<int:pk>/',views.appUserPublicView.as_view({'get':'retrieve'})),
   path('register/',views.appUserCreateView.as_view({'post':'create'})),
   path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
]