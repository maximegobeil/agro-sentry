import pytz
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

COUNTRY_CODES = [
    ("US", "United States"),
    ("CA", "Canada"),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name


class PhoneNumber(models.Model):
    PHONE_TYPE = [
        ("mobile", "Mobile"),
        ("landline", "Landline"),
        ("fax", "Fax"),
        ("business", "Business"),
        ("other", "Other"),
    ]

    phone_number = PhoneNumberField()
    phone_type = models.CharField(max_length=10, choices=PHONE_TYPE)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_notification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} ({self.phone_type})"


class Address(models.Model):
    ADDRESS_TYPE = [
        ("home", "Home"),
        ("office", "Office"),
        ("other", "Other"),
        ("billing", "Billing"),
        ("shipping", "Shipping"),
    ]

    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=255)
    unit_number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=3, choices=COUNTRY_CODES)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_type} - {self.street_number} {self.street_name} {self.unit_number}"

    def get_full_address(self):
        return f"{self.street_number} {self.street_name} {self.unit_number}, {self.city}, {self.state} {self.zipcode}, {self.country}"


class Organization(models.Model):
    SUBSCRIPTION_STATUS = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("trial", "Trial"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
    country = models.CharField(max_length=3, choices=COUNTRY_CODES)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=50, choices=TIMEZONE_CHOICES, default="America/New_York"
    )
    is_active = models.BooleanField(default=True)
    sub_status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS)
    sub_end_date = models.DateField(null=True, blank=True)
    max_stations = models.IntegerField(default=10)
    max_users = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationMembership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Administrator"),
        ("member", "Member"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "organization"]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"


class UserProfile(models.Model):
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System"),
    ]
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("es", "Spanish"),
        ("fr", "French"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    notification_email = models.CharField(max_length=255, blank=True)
    phone = models.ForeignKey(
        PhoneNumber, on_delete=models.CASCADE, blank=True, null=True
    )
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="system")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="en")
    timezone = models.CharField(
        max_length=50, choices=TIMEZONE_CHOICES, default="America/New_York"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.id}"


class Station(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Near water pump, to help identify the location",
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    altitude = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    last_seen = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NotificationPreference(models.Model):
    NOTIFICATION_METHOD = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("push", "Push"),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    notification_method = models.CharField(max_length=20, choices=NOTIFICATION_METHOD)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.user.email} - {self.station.name} ({self.notification_method})"


class SensorType(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_multi_value = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    calibration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.station.name} - {self.identifier}"


class AlertRule(models.Model):
    COMPARISON_CHOICES = [
        ("gt", "Greater Than"),
        ("lt", "Less Than"),
        ("gte", "Greater Than or Equal"),
        ("lte", "Less Than or Equal"),
        ("eq", "Equal"),
        ("neq", "Not Equal"),
    ]

    SEVERITY_CHOICES = [
        ("info", "Information"),
        ("warning", "Warning"),
        ("critical", "Critical"),
    ]

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comparison = models.CharField(max_length=10, choices=COMPARISON_CHOICES)
    value_key = models.CharField(
        max_length=255,
        help_text="JSON path to the value to check (e.g., 'temperature.celsius')",
    )
    threshold_value = models.JSONField(
        help_text="For 'between' comparison, provide [min, max]. For others, provide single value"
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="info")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.sensor.identifier}"

    def check_condition(self, sensor_data):
        """
        Evaluates if the alert condition is met based on sensor data

        Args:
            sensor_data (dict): JSON data from sensor reading

        Returns:
            bool: True if condition is met, False otherwise
        """
        try:
            # Navigate through nested dictionary using value_key
            value = sensor_data
            for key in self.value_key.split("."):
                value = value[key]

            if self.comparison == "between":
                min_val, max_val = self.threshold_value
                return min_val <= value <= max_val
            elif self.comparison == "not_between":
                min_val, max_val = self.threshold_value
                return value < min_val or value > max_val
            elif self.comparison == "gt":
                return value > self.threshold_value
            elif self.comparison == "lt":
                return value < self.threshold_value
            elif self.comparison == "gte":
                return value >= self.threshold_value
            elif self.comparison == "lte":
                return value <= self.threshold_value
            elif self.comparison == "eq":
                return value == self.threshold_value
            elif self.comparison == "neq":
                return value != self.threshold_value

            return False
        except (KeyError, TypeError, ValueError):
            return False
