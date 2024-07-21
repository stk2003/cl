from django.test import TestCase
from .forms import AppointmentForm, ClinicReviewForm, RegistrationForm
from .models import Service, Cost, Clinic, ClinicReview, Appointment

class ServiceModelTest(TestCase):
    def test_service_creation(self):
        service = Service.objects.create(
            name="test service",
            description="testing."
        )
        self.assertEqual(service.name, "test service")
        self.assertEqual(service.description, "testing.")

class CostModelTest(TestCase):
    def test_cost_creation(self):
        service = Service.objects.create(
            name="test service",
            description="testing."
        )
        cost = Cost.objects.create(
            service=service,
            cost_amount=50.0
        )
        self.assertEqual(cost.service, service)
        self.assertEqual(cost.cost_amount, 50.0)

class ClinicModelTest(TestCase):
    def test_clinic_creation(self):
        clinic = Clinic.objects.create(
            name="test clinic",
            address="test street",
            phone_number="12345678910",
            email="test@example.com",
            description="test desc."
        )
        self.assertEqual(clinic.name, "test clinic")
        self.assertEqual(clinic.address, "test street")
        self.assertEqual(clinic.phone_number, "12345678910")
        self.assertEqual(clinic.email, "test@example.com")
        self.assertEqual(clinic.description, "test desc.")

class ClinicReviewModelTest(TestCase):
    def test_clinic_review_creation(self):
        clinic = Clinic.objects.create(
            name="test clinic",
            address="test street",
            phone_number="12345678910",
            email="test@example.com",
            description="test desc."
        )
        review = ClinicReview.objects.create(
            clinic=clinic,
            rating=5,
            review_text="test review.",
            user_name="test user"
        )
        self.assertEqual(review.clinic, clinic)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.review_text, "test review.")
        self.assertEqual(review.user_name, "test user")

class AppointmentModelTest(TestCase):
    def test_appointment_creation(self):
        
        clinic = Clinic.objects.create(
            name="test clinic",
            address="test street",
            phone_number="12345678910",
            email="test@example.com",
            description="test desc."
        )
        service = Service.objects.create(
            name="test service",
            description="testing."
        )
        appointment = Appointment.objects.create(
            client_name="Ivan Ivanov",
            clinic=clinic,
            email="Ivan@example.com",
            phone_number="1234567890",
            appointment_date="2023-12-31T23:59",
        )
        appointment.service.add(service)
        self.assertEqual(appointment.client_name, "Ivan Ivanov")
        self.assertEqual(appointment.clinic, clinic)
        self.assertEqual(appointment.email, "Ivan@example.com")
        self.assertEqual(appointment.phone_number, "1234567890")
        self.assertEqual(appointment.appointment_date, "2023-12-31T23:59") 

class AppointmentFormTest(TestCase):
    
    def test_valid_appointment_form(self):
        service1 = Service.objects.create(
            name="test service",
            description="testing."
        )
        service2 = Service.objects.create(
            name="test service2",
            description="testing2."
        )
        form_data = {
            'client_name': 'Ivan Ivanov',
            'clinic': Clinic.objects.create(name='Test Clinic', address='Test Address', phone_number='12345678910', email='rightemail@clinic.com', description='norm clinic'),
            'email': 'ivan@example.com',
            'phone_number': '79345678912',
            'appointment_date': '2023-12-31T23:59',
            'service': [service1.id, service2.id],
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_appointment_form(self):
        form_data = {
            'client_name': 'Ivan Ivanov',
            'clinic': 'нет такой клиники)',
            'email': 'нет адреса',
            'phone_number': '79345678912',
            'appointment_date': 'завтра',
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())


class ClinicReviewFormTest(TestCase):
    def test_valid_clinic_review_form(self):
        form_data = {
            'clinic': Clinic.objects.   create(name='Test Clinic', address='Test Address', phone_number='12345678910', email='rightemail@clinic.com', description='norm clinic'),
            'rating': '5',
            'review_text': 'test review.',
            'user_name': 'test user',
        }
        form = ClinicReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_clinic_review_form(self):
        form_data = {
            'clinic': Clinic.objects.create(name='Test Clinic', address='Test Address', phone_number='12345678910', email='no email', description='norm clinic'),
            'rating': 'good',
            'review_text': 'test review.',
            'user_name': 'test user',
        }
        form = ClinicReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegistrationFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123321123',
            'password2': 'password123321123',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testemail',
            'password1': '123',
            'password2': '321',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

