from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('policy/', policy, name='policy'),
    path('certificates/', certificates, name='certificates'),
    
    # Пользователи
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    
    # Записи и отзывы
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('add-review/', add_review, name='add_review'),
    
    # Контакты
    path('contact/', contact, name='contact'),
    

]