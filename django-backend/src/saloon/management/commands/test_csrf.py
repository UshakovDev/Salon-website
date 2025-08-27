from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Проверяет настройки CSRF'

    def handle(self, *args, **options):
        self.stdout.write('🔒 Проверка настроек CSRF...')
        
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}')
        self.stdout.write(f'CSRF_COOKIE_SECURE: {getattr(settings, "CSRF_COOKIE_SECURE", "Не установлено")}')
        self.stdout.write(f'SESSION_COOKIE_SECURE: {getattr(settings, "SESSION_COOKIE_SECURE", "Не установлено")}')
        
        if settings.DEBUG:
            self.stdout.write(self.style.SUCCESS('✅ Режим отладки включен'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Режим отладки выключен'))
            
        self.stdout.write('🌐 Попробуйте зайти в админку: http://localhost:8080/admin/')
        self.stdout.write('👤 Логин: admin, Пароль: admin123')
