from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Services'


class Cost(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service.name} - {self.cost_amount} руб."

    class Meta:
        verbose_name_plural = 'Costs'


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = PhoneNumberField(region='RU')
    email = models.EmailField()
    description = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Clinics'


class ClinicReview(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=1, decimal_places=0)
    review_text = models.TextField()
    user_name = models.CharField(max_length=100)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.review_date.strftime('%Y-%m-%d %H:%M:%S')
        return f"Отзыв о {self.clinic.name} от {self.user_name} {formatted_date}"


class Appointment(models.Model):
    client_name = models.CharField(max_length=100)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = PhoneNumberField(region='RU')
    appointment_date = models.DateTimeField()
    service = models.ManyToManyField(Service)

    def __str__(self):
        return f"Запись на прием в отделении {self.client_name} на {self.appointment_date}"


class ClinicDescription(models.Model):
    description = models.TextField(unique=True)

    def __str__(self):
        return "Clinic Description"
