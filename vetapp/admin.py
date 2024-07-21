from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin

from .models import Clinic, ClinicReview, Service, Cost, Appointment, ClinicDescription


# Register your models here.

class ClinicReviewInline(admin.TabularInline):
    model = ClinicReview
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address', 'email')
    fields = ('name', 'phone_number', 'address', 'email')
    search_fields = ('name', 'phone_number', 'address', 'email')
    inlines = [ClinicReviewInline]


class ClinicReviewAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ClinicReview
    list_display = ('clinic', 'rating', 'review_text', 'user_name', 'review_date')
    readonly_fields = ('clinic', 'rating', 'review_text', 'user_name', 'review_date')
    list_filter = ('clinic',)
    fields = ('clinic', 'rating', 'review_text', 'user_name')
    search_fields = ('clinic', 'rating', 'review_text', 'user_name', 'review_date')
    date_hierarchy = 'review_date'


class CostInline(admin.TabularInline):
    model = Cost
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_cost', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'display_cost')

    inlines = [CostInline]

    @admin.display(description='Цена')  #
    def display_cost(self, obj):
        try:
            cost = Cost.objects.get(service=obj)
            return f"{cost.cost_amount} руб."
        except Cost.DoesNotExist:
            return "No cost available"


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'clinic', 'email', 'phone_number', 'appointment_date', 'display_services')
    list_display_links = ('client_name', 'clinic')
    raw_id_fields = ('clinic',)
    filter_horizontal = ('service',)
    list_filter = ('clinic', 'service')
    search_fields = ('client_name', 'email', 'phone_number')
    date_hierarchy = ('appointment_date')

    def display_services(self, obj):
        return ', '.join([str(service) for service in obj.service.all()])

    display_services.short_description = 'Услуги'


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(ClinicReview, ClinicReviewAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Cost)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ClinicDescription)
