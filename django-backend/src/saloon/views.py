from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils import timezone
from datetime import datetime

from .models import *
from .forms import *

menu = ["О нас", "Услуги", "Прайс", "Галерея", "Контакты"]

def index(request): #HttpRequest
    content = Immutable_content.objects.all()
    # categories = Category.objects.all()
    categories = Category.objects.prefetch_related('subcategories__pricelist_set').all()
    meta_tag = SiteContent.objects.values_list('description', flat=True).first() or ""


    image_queryset = Image.objects.filter(
        category__name__in=[
            'Брови', 'Депиляция', 'Пилинг', 'Аппаратная терапия',
            'Инъекционная терапия', 'Механическая чистка лица'
        ]
    ).select_related('category')

    image_galleries = {
        'brows': [],
        'depilation': [],
        'peeling': [],
        'ap_therapy': [],
        'in_therapy': [],
        'mechanical': []
    }

    category_mapping = {
        'Брови': 'brows',
        'Депиляция': 'depilation',
        'Пилинг': 'peeling',
        'Аппаратная терапия': 'ap_therapy',
        'Инъекционная терапия': 'in_therapy',
        'Механическая чистка лица': 'mechanical',
    }

    for image in image_queryset:
        category_name = image.category.name
        key = category_mapping[category_name]
        image_galleries[key].append(image.image.url)

    import json
    image_galleries = json.dumps(image_galleries)

    return render(request, 'saloon/index.html', {
        'menu': menu,
        'title': 'Салон красоты Queen cosmo | Лучший салон красоты в городе Зея', # улучшить для сео
        'content': content,
        'categories': categories,
        'image_galleries': image_galleries,
        'meta': meta_tag
    })

@cache_page(60 * 15)
def certificates(request):
    Certificat = Certificates.objects.all()
    return render(request, 'saloon/certificates.html', {
        'title': 'Сертификаты | Салон красоты Зея Queen cosmo',
        'Certificat': Certificat
    })
@cache_page(60 * 15)
def policy(request):
    try:
        # Пытаемся получить политику конфиденциальности
        Policy = PrivacyPolicy.objects.get(id=1)
        data_collection = DataCollection.objects.filter(policy=Policy)
        third_party_data = ThirdPartyDataTransfer.objects.filter(policy=Policy)
    except PrivacyPolicy.DoesNotExist:
        # Если данных нет, используем пустые значения
        Policy = None
        data_collection = []
        third_party_data = []

    return render(request, 'saloon/policy.html', {
        'title': 'Политика конфиденциальности | Салон красоты Зея Queen cosmo',
        'policy': Policy,
        'data_collection': data_collection,
        'third_party_data': third_party_data
    })

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')  # ошибка 404

# Функции для работы с пользователями
def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                
                # Создаем профиль пользователя салона
                salon_user = SalonUser.objects.create(
                    user=user,
                    phone=form.cleaned_data.get('phone', ''),
                    birth_date=form.cleaned_data.get('birth_date'),
                    gender=form.cleaned_data.get('gender', ''),
                    address=form.cleaned_data.get('address', '')
                )
                
                # Автоматически входим в систему
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}! Регистрация прошла успешно.')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Ошибка при создании пользователя: {str(e)}')
        else:
            # Выводим ошибки валидации
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле {field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'saloon/register.html', {
        'form': form,
        'title': 'Регистрация | Салон красоты Queen Cosmo'
    })


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                return redirect('profile')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            # Выводим ошибки валидации
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле {field}: {error}')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'saloon/login.html', {
        'form': form,
        'title': 'Вход | Салон красоты Queen Cosmo'
    })


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')


@login_required
def profile(request):
    """Профиль пользователя"""
    try:
        salon_user = SalonUser.objects.get(user=request.user)
    except SalonUser.DoesNotExist:
        # Если профиль не существует, создаем его
        salon_user = SalonUser.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = SalonUserProfileForm(request.POST, instance=salon_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = SalonUserProfileForm(instance=salon_user)
    
    # Получаем записи пользователя
    appointments = Appointment.objects.filter(client=salon_user).order_by('-appointment_date')
    reviews = Review.objects.filter(user=salon_user).order_by('-created_at')
    
    return render(request, 'saloon/profile.html', {
        'salon_user': salon_user,
        'form': form,
        'appointments': appointments,
        'reviews': reviews,
        'title': 'Мой профиль | Салон красоты Queen Cosmo'
    })


@login_required
def book_appointment(request):
    """Запись на услугу"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                salon_user = SalonUser.objects.get(user=request.user)
                
                # Создаем запись
                appointment = Appointment.objects.create(
                    client=salon_user,
                    service=form.cleaned_data['service'],
                    appointment_date=datetime.combine(
                        form.cleaned_data['preferred_date'],
                        form.cleaned_data['preferred_time']
                    ),
                    notes=form.cleaned_data.get('notes', '')
                )
                
                messages.success(request, f'Запись на {appointment.service.name} успешно создана!')
                return redirect('profile')
                
            except SalonUser.DoesNotExist:
                messages.error(request, 'Профиль пользователя не найден.')
    else:
        form = AppointmentForm()
    
    return render(request, 'saloon/book_appointment.html', {
        'form': form,
        'title': 'Запись на услугу | Салон красоты Queen Cosmo'
    })


@login_required
def add_review(request):
    """Добавление отзыва"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                salon_user = SalonUser.objects.get(user=request.user)
                
                review = Review.objects.create(
                    user=salon_user,
                    service=form.cleaned_data.get('service'),
                    rating=form.cleaned_data['rating'],
                    text=form.cleaned_data['text']
                )
                
                messages.success(request, 'Ваш отзыв успешно добавлен и ожидает модерации!')
                return redirect('profile')
                
            except SalonUser.DoesNotExist:
                messages.error(request, 'Профиль пользователя не найден.')
    else:
        form = ReviewForm()
    
    return render(request, 'saloon/add_review.html', {
        'form': form,
        'title': 'Добавить отзыв | Салон красоты Queen Cosmo'
    })


def contact(request):
    """Форма обратной связи"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику отправки email или сохранения в базу
            messages.success(request, 'Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'saloon/contact.html', {
        'form': form,
        'title': 'Контакты | Салон красоты Queen Cosmo'
    })




