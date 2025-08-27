from django.core.management.base import BaseCommand
from saloon.models import *


class Command(BaseCommand):
    help = 'Очищает сайт от тестовых данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Удалить все данные (не только тестовые)',
        )

    def handle(self, *args, **options):
        if options['all']:
            self.stdout.write('🗑️ Удаляю ВСЕ данные из базы...')
            self.clear_all_data()
        else:
            self.stdout.write('🧹 Удаляю только тестовые данные...')
            self.clear_test_data()
        
        self.stdout.write(self.style.SUCCESS('✅ Очистка завершена!'))

    def clear_test_data(self):
        """Удаляет только тестовые данные"""
        # Удаляем тестовые изображения
        test_images = Image.objects.filter(image__startswith='photos/test/')
        count = test_images.count()
        test_images.delete()
        self.stdout.write(f'   🖼️ Удалено {count} тестовых изображений')
        
        # Удаляем тестовые сертификаты
        test_certs = Certificates.objects.filter(image__startswith='photos/certificates/certificate_')
        count = test_certs.count()
        test_certs.delete()
        self.stdout.write(f'   🏆 Удалено {count} тестовых сертификатов')
        
        # Удаляем тестовый контент
        test_content = Immutable_content.objects.filter(
            title__in=['Главный заголовок', 'О нас', 'Почему выбирают нас']
        )
        count = test_content.count()
        test_content.delete()
        self.stdout.write(f'   📝 Удалено {count} тестовых блоков контента')
        
        # Удаляем тестовые мета-теги
        test_meta = SiteContent.objects.filter(
            page_name__in=['Главная страница', 'Услуги', 'Галерея', 'Контакты']
        )
        count = test_meta.count()
        test_meta.delete()
        self.stdout.write(f'   🏷️ Удалено {count} тестовых мета-тегов')

    def clear_all_data(self):
        """Удаляет все данные из базы"""
        # Удаляем все данные в правильном порядке (из-за foreign keys)
        
        # Сначала удаляем зависимые модели
        PriceList.objects.all().delete()
        self.stdout.write('   💰 Удален весь прайс-лист')
        
        Image.objects.all().delete()
        self.stdout.write('   🖼️ Удалены все изображения')
        
        Certificates.objects.all().delete()
        self.stdout.write('   🏆 Удалены все сертификаты')
        
        DataCollection.objects.all().delete()
        ThirdPartyDataTransfer.objects.all().delete()
        PrivacyPolicy.objects.all().delete()
        self.stdout.write('   🔒 Удалена политика конфиденциальности')
        
        # Затем удаляем основные модели
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write('   🏷️ Удалены все категории услуг')
        
        ImageCategory.objects.all().delete()
        self.stdout.write('   📸 Удалены все категории фото')
        
        Immutable_content.objects.all().delete()
        self.stdout.write('   📝 Удален весь контент')
        
        SiteContent.objects.all().delete()
        self.stdout.write('   🏷️ Удалены все мета-теги')
        
        self.stdout.write('   ✅ Все данные удалены из базы')
