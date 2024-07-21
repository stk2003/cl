from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, redirect
from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import ClinicReviewForm, AppointmentForm, RegistrationForm, UserAuthenticationForm
from .models import Service, Cost, Clinic, ClinicReview, Appointment, ClinicDescription
from .serializers import (
    ServiceSerializer, CostSerializer, ClinicSerializer,
    ClinicReviewSerializer, AppointmentSerializer, ClinicDescriptionSerializer
)
from django.shortcuts import render


def home(request):
    return render(request, 'about.html')


def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def contact(request):
    clinic_info = Clinic.objects.all()
    return render(request, 'contacts.html', {'clinics': clinic_info})


def home(request):
    return render(request, 'base.html')


def about(request):
    description = ClinicDescription.objects.first()
    return render(request, 'about.html', {'client_description': description})


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.email = request.user.email
            appointment.save()
            form.save_m2m()
            messages.success(request, 'Ваша запись на прием была отправлена.')
            return redirect('book_appointment')
    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form})


def review_clinic(request):
    reviews = ClinicReview.objects.all()
    if request.method == 'POST':
        form = ClinicReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('review_clinic')
    else:
        form = ClinicReviewForm()

    return render(request, 'review_page.html', {'form': form, 'reviews': reviews})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


def UserLogin(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def UserLogout(request):
    logout(request)
    return redirect('home')


@login_required
def appointment_history(request):
    appointments = Appointment.objects.filter(email=request.user.email)
    for appointment in appointments:
        total_cost = appointment.service.aggregate(total_cost=Sum('cost__cost_amount'))['total_cost']
        appointment.total_cost = total_cost

    return render(request, 'appointment_history.html', {'appointments': appointments})


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class CostViewSet(viewsets.ModelViewSet):
    queryset = Cost.objects.all()
    serializer_class = CostSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['name', 'address']

    @action(detail=True, methods=['POST'])
    def add_review(self, request, pk=None):
        clinic = self.get_object()
        review_data = request.data.copy()  # Копируем данные запроса
        review_data['clinic'] = clinic.pk  # Устанавливаем идентификатор клиники в данные отзыва
        review_serializer = ClinicReviewSerializer(data=review_data)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(review_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', None)
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset


class ClinicReviewViewSet(viewsets.ModelViewSet):
    queryset = ClinicReview.objects.all()
    serializer_class = ClinicReviewSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class ClinicDescriptionViewSet(viewsets.ModelViewSet):
    queryset = ClinicDescription.objects.all()
    serializer_class = ClinicDescriptionSerializer
