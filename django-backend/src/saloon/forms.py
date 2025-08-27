from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import SalonUser, Appointment, Review, PriceList


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')
    birth_date = forms.DateField(required=False, label='Дата рождения', 
                                widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=SalonUser.GENDER_CHOICES, required=False, label='Пол')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Адрес')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Кастомизация полей
        self.fields['username'].help_text = 'Обязательно. 150 символов или меньше. Только буквы, цифры и символы @/./+/-/_'
        self.fields['password1'].help_text = 'Ваш пароль должен содержать как минимум 8 символов'
        self.fields['password2'].help_text = 'Введите тот же пароль, что и выше, для проверки'
        
        # Добавляем CSS классы ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа пользователя"""
    username = forms.CharField(label='Имя пользователя или Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class SalonUserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""
    class Meta:
        model = SalonUser
        fields = ['phone', 'birth_date', 'gender', 'address', 'notes']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class AppointmentForm(forms.ModelForm):
    """Форма записи на услугу"""
    preferred_date = forms.DateField(label='Предпочитаемая дата', 
                                   widget=forms.DateInput(attrs={'type': 'date'}))
    preferred_time = forms.TimeField(label='Предпочитаемое время',
                                   widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = Appointment
        fields = ['service', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительные пожелания или комментарии'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только активные услуги
        self.fields['service'].queryset = PriceList.objects.all().order_by('subcategory__category__name', 'subcategory__name')
    
    def clean(self):
        cleaned_data = super().clean()
        preferred_date = cleaned_data.get('preferred_date')
        preferred_time = cleaned_data.get('preferred_time')
        
        if preferred_date and preferred_time:
            from datetime import datetime, timedelta
            now = datetime.now()
            appointment_datetime = datetime.combine(preferred_date, preferred_time)
            
            # Проверяем, что дата не в прошлом
            if appointment_datetime < now:
                raise forms.ValidationError('Нельзя записаться на прошедшую дату')
            
            # Проверяем, что дата не слишком далеко в будущем (например, не более года)
            if appointment_datetime > now + timedelta(days=365):
                raise forms.ValidationError('Нельзя записаться более чем на год вперед')
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Review
        fields = ['service', 'rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Поделитесь своими впечатлениями об услуге...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем услуги
        self.fields['service'].queryset = PriceList.objects.all().order_by('subcategory__category__name', 'subcategory__name')
        self.fields['service'].required = False  # Отзыв может быть общий, не привязанный к конкретной услуге


class ContactForm(forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(max_length=100, label='Ваше имя', required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(max_length=20, label='Телефон', required=False)
    subject = forms.CharField(max_length=200, label='Тема', required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Сообщение', required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS классы
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
