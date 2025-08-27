from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from saloon.models import *
import os


class Command(BaseCommand):
    help = 'Заполняет сайт тестовыми данными для демонстрации'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Начинаю заполнение сайта тестовыми данными...')
        
        # 1. Создаем основной контент
        self.create_immutable_content()
        
        # 2. Создаем категории услуг
        self.create_categories()
        
        # 3. Создаем прайс-лист
        self.create_price_list()
        
        # 4. Создаем категории фото
        self.create_image_categories()
        
        # 5. Создаем тестовые изображения (заглушки)
        self.create_test_images()
        
        # 6. Создаем политику конфиденциальности
        self.create_privacy_policy()
        
        # 7. Создаем сертификаты
        self.create_certificates()
        
        # 8. Создаем мета-теги
        self.create_site_content()
        
        self.stdout.write(self.style.SUCCESS('✅ Сайт успешно заполнен тестовыми данными!'))
        self.stdout.write('🌐 Откройте http://localhost:8080 для просмотра')

    def create_immutable_content(self):
        """Создает основной контент для главной страницы"""
        self.stdout.write('📝 Создаю основной контент...')
        
        content_data = [
            {
                'id': 1,
                'title': 'Главный заголовок',
                'content': 'Добро пожаловать в студию красоты Queen Cosmo! Мы предлагаем широкий спектр услуг для вашей красоты.'
            },
            {
                'id': 2,
                'title': 'Профессиональный опыт',
                'content': 'Наши мастера имеют многолетний опыт работы в индустрии красоты. Каждый специалист регулярно проходит обучение и повышает квалификацию, чтобы предложить вам самые современные и эффективные процедуры.'
            },
            {
                'id': 3,
                'title': 'Индивидуальный подход',
                'content': 'Мы понимаем, что каждый клиент уникален. Поэтому разрабатываем индивидуальную программу ухода, учитывая особенности вашей кожи, возраст и пожелания. Ваша красота - наш приоритет.'
            },
            {
                'id': 4,
                'title': 'Качественные материалы',
                'content': 'Используем только сертифицированные материалы и косметику премиум-класса от ведущих мировых брендов. Безопасность и эффективность - основа нашего подхода к красоте.'
            },
            {
                'id': 5,
                'title': 'О нас - часть 1',
                'content': 'Студия красоты Queen Cosmo была основана в 2018 году с целью создания пространства, где каждая женщина может почувствовать себя особенной и красивой.'
            },
            {
                'id': 6,
                'title': 'О нас - часть 2',
                'content': 'Мы находимся в центре города Зея, в удобном ТЦ "Городок" на 2 этаже. Наша студия оборудована современной техникой и создает комфортную атмосферу для всех процедур.'
            },
            {
                'id': 7,
                'title': 'О нас - часть 3',
                'content': 'За годы работы мы помогли тысячам клиенток обрести уверенность в себе и подчеркнуть свою естественную красоту. Доверьте свою красоту профессионалам!'
            }
        ]
        
        for data in content_data:
            Immutable_content.objects.get_or_create(
                id=data['id'],
                defaults={
                    'title': data['title'],
                    'content': data['content']
                }
            )
        
        self.stdout.write('   ✅ Основной контент создан')

    def create_categories(self):
        """Создает категории услуг"""
        self.stdout.write('🏷️ Создаю категории услуг...')
        
        categories_data = [
            'Лицо',
            'Тело', 
            'Брови и ресницы',
            'Макияж',
            'Маникюр и педикюр',
            'Массаж'
        ]
        
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(name=cat_name)
            
            # Создаем подкатегории для каждой категории
            if cat_name == 'Лицо':
                subcategories = ['Очищение', 'Увлажнение', 'Омоложение', 'Пилинг']
            elif cat_name == 'Тело':
                subcategories = ['Депиляция', 'Обертывания', 'Массаж', 'Уход за кожей']
            elif cat_name == 'Брови и ресницы':
                subcategories = ['Коррекция бровей', 'Окрашивание бровей', 'Наращивание ресниц', 'Ламинирование']
            elif cat_name == 'Макияж':
                subcategories = ['Дневной макияж', 'Вечерний макияж', 'Свадебный макияж', 'Макияж для фотосессии']
            elif cat_name == 'Маникюр и педикюр':
                subcategories = ['Классический маникюр', 'Аппаратный маникюр', 'Педикюр', 'Дизайн ногтей']
            elif cat_name == 'Массаж':
                subcategories = ['Классический массаж', 'Антицеллюлитный массаж', 'Расслабляющий массаж', 'Спортивный массаж']
            
            for sub_name in subcategories:
                Subcategory.objects.get_or_create(
                    name=sub_name,
                    category=category
                )
        
        self.stdout.write('   ✅ Категории и подкатегории созданы')

    def create_price_list(self):
        """Создает прайс-лист услуг"""
        self.stdout.write('💰 Создаю прайс-лист...')
        
        # Получаем подкатегории
        subcategories = Subcategory.objects.all()
        
        price_data = [
            # Лицо
            ('Очищение', 'Ультразвуковая чистка лица', 1500, 2500),
            ('Очищение', 'Механическая чистка лица', 2000, 3000),
            ('Увлажнение', 'Увлажняющая маска', 800, 1200),
            ('Омоложение', 'Ботокс', 3000, 5000),
            ('Омоложение', 'Филлеры', 5000, 8000),
            ('Пилинг', 'Химический пилинг', 2000, 3500),
            ('Пилинг', 'Фруктовый пилинг', 1500, 2500),
            
            # Тело
            ('Депиляция', 'Депиляция ног', 1500, 2500),
            ('Депиляция', 'Депиляция рук', 800, 1200),
            ('Депиляция', 'Депиляция подмышек', 500, 800),
            ('Обертывания', 'Водорослевое обертывание', 2000, 3000),
            ('Обертывания', 'Шоколадное обертывание', 2500, 3500),
            ('Массаж', 'Антицеллюлитный массаж', 2000, 3000),
            ('Массаж', 'Расслабляющий массаж', 1500, 2500),
            
            # Брови и ресницы
            ('Коррекция бровей', 'Коррекция бровей', 500, 800),
            ('Окрашивание бровей', 'Окрашивание бровей', 800, 1200),
            ('Наращивание ресниц', 'Наращивание ресниц', 2000, 3500),
            ('Ламинирование', 'Ламинирование бровей', 1500, 2500),
            
            # Макияж
            ('Дневной макияж', 'Дневной макияж', 1500, 2500),
            ('Вечерний макияж', 'Вечерний макияж', 2000, 3500),
            ('Свадебный макияж', 'Свадебный макияж', 3000, 5000),
            ('Макияж для фотосессии', 'Макияж для фотосессии', 2500, 4000),
            
            # Маникюр и педикюр
            ('Классический маникюр', 'Классический маникюр', 800, 1200),
            ('Аппаратный маникюр', 'Аппаратный маникюр', 1200, 1800),
            ('Педикюр', 'Педикюр', 1500, 2500),
            ('Дизайн ногтей', 'Дизайн ногтей', 500, 1000),
        ]
        
        for sub_name, service_name, min_price, max_price in price_data:
            try:
                subcategory = Subcategory.objects.get(name=sub_name)
                PriceList.objects.get_or_create(
                    service_title=service_name,
                    subcategory=subcategory,
                    defaults={
                        'min_price': min_price,
                        'max_price': max_price
                    }
                )
            except Subcategory.DoesNotExist:
                continue
        
        self.stdout.write('   ✅ Прайс-лист создан')

    def create_image_categories(self):
        """Создает категории для фотографий работ"""
        self.stdout.write('📸 Создаю категории фото...')
        
        image_categories = [
            'Брови',
            'Депиляция', 
            'Пилинг',
            'Аппаратная терапия',
            'Инъекционная терапия',
            'Механическая чистка лица',
            'Макияж',
            'Маникюр',
            'Массаж'
        ]
        
        for cat_name in image_categories:
            ImageCategory.objects.get_or_create(name=cat_name)
        
        self.stdout.write('   ✅ Категории фото созданы')

    def create_test_images(self):
        """Создает тестовые изображения (заглушки)"""
        self.stdout.write('🖼️ Создаю тестовые изображения...')
        
        # Создаем тестовые изображения для каждой категории
        image_categories = ImageCategory.objects.all()
        
        for category in image_categories:
            # Создаем 2-3 изображения для каждой категории
            for i in range(2):
                # Создаем заглушку для изображения
                image_name = f"test_{category.name.lower()}_{i+1}.jpg"
                
                # Проверяем, не существует ли уже такое изображение
                if not Image.objects.filter(category=category, image__contains=f"test_{category.name.lower()}_{i+1}"):
                    # Создаем запись в базе данных
                    Image.objects.get_or_create(
                        category=category,
                        image=f"photos/test/{image_name}"
                    )
        
        self.stdout.write('   ✅ Тестовые изображения созданы (заглушки)')

    def create_privacy_policy(self):
        """Создает политику конфиденциальности"""
        self.stdout.write('🔒 Создаю политику конфиденциальности...')
        
        policy, created = PrivacyPolicy.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Политика конфиденциальности',
                'description': 'Мы уважаем вашу конфиденциальность и обязуемся защищать ваши персональные данные.'
            }
        )
        
        if created:
            # Создаем данные о сборе информации
            DataCollection.objects.get_or_create(
                policy=policy,
                data='Имя, телефон, email, история посещений'
            )
            
            # Создаем данные о передаче третьим лицам
            ThirdPartyDataTransfer.objects.get_or_create(
                policy=policy,
                reason='Передача данных осуществляется только с вашего согласия для оказания услуг'
            )
        
        self.stdout.write('   ✅ Политика конфиденциальности создана')

    def create_certificates(self):
        """Создает тестовые сертификаты"""
        self.stdout.write('🏆 Создаю сертификаты...')
        
        # Создаем несколько тестовых сертификатов
        for i in range(3):
            Certificates.objects.get_or_create(
                image=f"photos/certificates/certificate_{i+1}.jpg"
            )
        
        self.stdout.write('   ✅ Сертификаты созданы')

    def create_site_content(self):
        """Создает мета-теги для сайта"""
        self.stdout.write('🏷️ Создаю мета-теги...')
        
        meta_content = [
            {
                'page_name': 'Главная страница',
                'description': 'Салон красоты Queen Cosmo в городе Зея. Широкий спектр услуг: ботокс, филлеры, депиляция, макияж, маникюр, массаж. Профессиональные мастера, качественные материалы.'
            },
            {
                'page_name': 'Услуги',
                'description': 'Услуги салона красоты Queen Cosmo: косметология, депиляция, макияж, маникюр, массаж. Подробные описания и цены на все услуги.'
            },
            {
                'page_name': 'Галерея',
                'description': 'Галерея работ салона красоты Queen Cosmo. Фотографии до и после процедур, примеры работ наших мастеров.'
            },
            {
                'page_name': 'Контакты',
                'description': 'Контакты салона красоты Queen Cosmo в городе Зея. Адрес, телефон, режим работы, как добраться.'
            }
        ]
        
        for data in meta_content:
            SiteContent.objects.get_or_create(
                page_name=data['page_name'],
                defaults={'description': data['description']}
            )
        
        self.stdout.write('   ✅ Мета-теги созданы')
