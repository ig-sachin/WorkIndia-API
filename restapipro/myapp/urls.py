from django.urls import path
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI
from . import views

urlpatterns = [
    # Url for User Auth
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),

    # Url for Blocking User
    path('api/logoutuserbyadmin/', views.logout_request, name='logout'),

    # Url's for Questions
    path('app/questions/', views.add_question, name='add-ques'),
    path('app/questions/<str:tags>/<str:text>/',
         views.getByTagsText, name='add-ques'),
    path('app/getall/',
         views.getAll, name='add-ques'),
    path('app/getid/<int:pk>/', views.getId, name='get-with-id'),
    path('app/update/<int:pk>/', views.update_items, name='update-items'),
    path('app/delete/<int:pk>/', views.delete_items, name='delete-items'),

    # Frontend
    path('home/', views.home, name='home'),
]
