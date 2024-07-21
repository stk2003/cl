from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from .models import Appointment, ClinicReview, Service

class AppointmentForm(forms.ModelForm):
    service = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label = 'Услуги',
    )
    phone_number = PhoneNumberField(region='RU',label = 'Телефонный номер')
    class Meta:
        model = Appointment
        fields = ['client_name', 'clinic', 'phone_number', 'appointment_date', 'service']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }   
        labels = {
            'client_name': 'Ваше имя',
            'clinic' : 'Выберите отделение',
            'email': 'Электронный адрес',
            'appointment_date': 'Дата и время приема',
        }

class ClinicReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(x, x) for x in range(0, 6)],
        label = 'Оценка',
        )
    class Meta:
        model = ClinicReview
        fields = ['clinic', 'rating', 'review_text', 'user_name']
        labels = {
            'clinic': 'Выберите отделение',
            'review_text': 'Ваш отзыв',
            'user_name': 'Ваше имя',
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Необходимое поле. Введите корректный электронный адрес.')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Данный электронный адрес уже зарегестрирован.')

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('Данное имя пользователя уже занято. Пожалуйста выберите другое')
        
        return username


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
