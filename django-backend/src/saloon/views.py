from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .models import *

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

