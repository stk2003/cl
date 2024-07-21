import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from vetapp.models import Appointment


@shared_task
def check_appointments():
    appointments = Appointment.objects.filter(appointment_date__gt=datetime.date.today())
    print(appointments)
    for appointment in appointments:
        send_mail(
            subject=appointment.service.name,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[appointment.email],
            message=f"Вы записаны на {appointment.appointment_date}",
        )
