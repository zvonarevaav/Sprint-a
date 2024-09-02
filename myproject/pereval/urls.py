from django.urls import path
from . import views
from django.http import HttpResponse

# Простое представление для pereval/
def pereval_home(request):
    return HttpResponse("Welcome to the Pereval section!")

urlpatterns = [
    path('', pereval_home),  # Корневой маршрут для /pereval/
    path('submitData/', views.submit_data, name='submit_data'),  # Маршрут для submitData
    path('submitData/<int:id>/', views.get_pereval, name='get_pereval'),  # Маршрут для GET /submitData/<id>
    path('submitData/<int:id>/edit/', views.update_pereval, name='update_pereval'),  # Маршрут для PATCH /submitData/<id>
    path('submitData/', views.get_perevals_by_user, name='get_perevals_by_user'),  # Маршрут для GET /submitData/?user__email=<email>
]
