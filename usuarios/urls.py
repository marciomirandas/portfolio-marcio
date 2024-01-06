from django.urls import path
from .views import login, registrar, logout, senha


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registrar/', registrar, name='registrar'),
    path('senha/', senha, name='senha'),
]
