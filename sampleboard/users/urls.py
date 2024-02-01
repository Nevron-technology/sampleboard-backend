from django.urls import include, path
from .views import  CustomAuthToken


urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view(), name='authentication'),
]