from django.urls import path
from . import views


urlpatterns = [
    path('', views.movie_recomendation_view, name='recommendations'),
]
