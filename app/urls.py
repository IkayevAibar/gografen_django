from django.urls import include,path
from app import views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime


urlpatterns = [
    path('user/<int:pk>/',views.appUserView.as_view({'get':'retrieve','put':'update'})),
    path('<int:pk>/',views.appUserPublicView.as_view({'get':'retrieve'})),
    path('register/',views.appUserCreateView.as_view({'post':'create'})),
    # path('auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),

    
]
