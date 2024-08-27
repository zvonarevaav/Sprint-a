from django.urls import path
from . import views
from django.http import HttpResponse

# Простое представление для pereval/
def pereval_home(request):
    return HttpResponse("Welcome to the Pereval section!")

urlpatterns = [
    path('', pereval_home),  # Корневой маршрут для /pereval/
    path('submitData/', views.submit_data, name='submit_data'),  # Маршрут для submitData
]
