from rest_framework import serializers
from .models import Service, Cost, Clinic, ClinicReview, Appointment, ClinicDescription


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'image_path']


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = ['id', 'service', 'cost_amount']

    def validate(self, data):
        if data['cost_amount'] <= 0:
            raise serializers.ValidationError("Стоимость должна быть больше нуля")
        return data


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'description']


class ClinicReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicReview
        fields = ['id', 'clinic', 'rating', 'review_text', 'user_name', 'review_date']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'client_name', 'clinic', 'email', 'phone_number', 'appointment_date', 'service']


class ClinicDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicDescription
        fields = ['id', 'description']
