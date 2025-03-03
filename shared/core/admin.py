import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (
    Address,
    AlertRule,
    CustomUser,
    NotificationPreference,
    Organization,
    OrganizationMembership,
    PhoneNumber,
    Sensor,
    SensorType,
    Station,
    UserProfile,
)

if getattr(settings, "ADMIN_ENABLED", False):

    @admin.register(CustomUser)
    class CustomUserAdmin(UserAdmin):
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm
        model = CustomUser
        list_display = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        )
        list_filter = (
            "is_staff",
            "is_active",
        )
        fieldsets = (
            (None, {"fields": ("email", "password")}),
            ("Personal info", {"fields": ("first_name", "last_name")}),
            (
                "Permissions",
                {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
            ),
        )
        add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": (
                        "email",
                        "first_name",
                        "last_name",
                        "password1",
                        "password2",
                        "is_staff",
                        "is_active",
                    ),
                },
            ),
        )
        search_fields = ("email", "first_name", "last_name")
        ordering = ("email",)

    @admin.register(PhoneNumber)
    class PhoneNumberAdmin(admin.ModelAdmin):
        list_display = (
            "phone_number",
            "phone_type",
            "is_primary",
            "is_verified",
        )
        list_filter = ("phone_type", "is_primary", "is_verified")

    @admin.register(Address)
    class AddressAdmin(admin.ModelAdmin):
        list_display = (
            "address_type",
            "city",
            "state",
            "country",
            "is_primary",
        )
        list_filter = ("address_type", "country", "is_primary")
        search_fields = (
            "street_name",
            "city",
            "state",
            "zipcode",
        )

    @admin.register(Organization)
    class OrganizationAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "country",
            "is_active",
            "sub_status",
            "max_stations",
            "max_users",
        )
        list_filter = ("is_active", "sub_status", "country")
        search_fields = ("name", "legal_name", "email")

    @admin.register(OrganizationMembership)
    class OrganizationMembershipAdmin(admin.ModelAdmin):
        list_display = ("user", "organization", "role", "is_primary")
        list_filter = ("role", "is_primary")
        search_fields = ("user__email", "organization__name")

    @admin.register(UserProfile)
    class UserProfileAdmin(admin.ModelAdmin):
        list_display = ("user", "theme", "language", "timezone")
        list_filter = ("theme", "language")
        search_fields = ("user__email", "notification_email")

    @admin.register(Station)
    class StationAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "organization",
            "location_name",
            "is_active",
            "last_seen",
        )
        list_filter = ("is_active", "organization")
        search_fields = ("name", "location_name")

    @admin.register(NotificationPreference)
    class NotificationPreferenceAdmin(admin.ModelAdmin):
        list_display = ("user_profile", "station", "notification_method", "is_active")
        list_filter = ("notification_method", "is_active")
        search_fields = ("user_profile__user__email", "station__name")

    @admin.register(SensorType)
    class SensorTypeAdmin(admin.ModelAdmin):
        list_display = ("name", "unit", "is_multi_value")
        list_filter = ("is_multi_value",)
        search_fields = ("name", "description")

    @admin.register(Sensor)
    class SensorAdmin(admin.ModelAdmin):
        list_display = (
            "identifier",
            "station",
            "sensor_type",
            "is_active",
            "calibration_date",
        )
        list_filter = ("is_active", "sensor_type", "station")
        search_fields = ("identifier", "station__name")

    @admin.register(AlertRule)
    class AlertRuleAdmin(admin.ModelAdmin):
        list_display = ("name", "sensor", "comparison", "severity", "is_active")
        list_filter = ("comparison", "severity", "is_active")
        search_fields = ("name", "sensor__identifier")
