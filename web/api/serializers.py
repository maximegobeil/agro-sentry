from core.models import Address, Organization, OrganizationMembership, PhoneNumber
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Extra info added along access and refresh
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address_type",
            "street_number",
            "street_name",
            "unit_number",
            "city",
            "state",
            "zipcode",
            "country",
        ]


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ["id", "phone_number"]


class OrganizationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    phone_number = PhoneNumberSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "legal_name",
            "description",
            "email",
            "country",
            "timezone",
            "sub_status",
            "sub_end_date",
            "max_stations",
            "max_users",
            "address",
            "phone_number",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name"]
        read_only_fields = ["email"]


class OrganizationMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationMembership
        fields = ["id", "user", "role", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]


class OrganizationStatsSerializer(serializers.ModelSerializer):
    total_stations = serializers.IntegerField(read_only=True)
    total_sensors = serializers.IntegerField(read_only=True)
    total_notifications = serializers.IntegerField(read_only=True)
    sensor_type_distribution = serializers.DictField(read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "total_stations",
            "total_sensors",
            "total_notifications",
            "sensor_type_distribution",
        ]
