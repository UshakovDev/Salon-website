# Generated manually for adding user models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saloon', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalonUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Телефон')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский'), ('O', 'Другой')], max_length=1, verbose_name='Пол')),
                ('address', models.TextField(blank=True, verbose_name='Адрес')),
                ('notes', models.TextField(blank=True, verbose_name='Заметки')),
                ('is_vip', models.BooleanField(default=False, verbose_name='VIP клиент')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь салона',
                'verbose_name_plural': 'Пользователи салона',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField(verbose_name='Дата и время записи')),
                ('status', models.CharField(choices=[('pending', 'Ожидает подтверждения'), ('confirmed', 'Подтверждено'), ('completed', 'Завершено'), ('cancelled', 'Отменено')], default='pending', max_length=20, verbose_name='Статус')),
                ('notes', models.TextField(blank=True, verbose_name='Заметки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saloon.salonuser', verbose_name='Клиент')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saloon.pricelist', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Запись на услугу',
                'verbose_name_plural': 'Записи на услуги',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 звезда'), (2, '2 звезды'), (3, '3 звезды'), (4, '4 звезды'), (5, '5 звезд')], verbose_name='Оценка')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Одобрен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saloon.salonuser', verbose_name='Клиент')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='saloon.pricelist', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
