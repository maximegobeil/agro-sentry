from core.models import Organization, OrganizationMembership, Sensor
from django.db.models import Count
from rest_framework import mixins, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomTokenObtainPairSerializer,
    OrganizationMemberSerializer,
    OrganizationSerializer,
    OrganizationStatsSerializer,
)

""" Auth """


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


""" Organization """


class OrganizationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(
            organizationmembership__user=self.request.user
        )


class OrganizationMembershipViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationMemberSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get("pk")

        if organization_id:
            return OrganizationMembership.objects.filter(
                organization_id=organization_id
            ).select_related("user")
        else:
            return OrganizationMembership.objects.none()


class OrganizationStatsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationStatsSerializer

    def retrieve(self, request, *args, **kwargs):
        organization_id = self.kwargs.get("pk")

        try:
            instance = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        instance = (
            Organization.objects.filter(id=organization_id)
            .annotate(
                total_stations=Count("station", distinct=True),
                total_sensors=Count("station__sensor", distinct=True),
                total_notifications=Count(
                    "station__notificationpreference", distinct=True
                ),
            )
            .first()
        )

        serializer = self.get_serializer(instance)
        data = serializer.data

        sensor_distribution = (
            Sensor.objects.filter(station__organization=instance)
            .values("sensor_type__name")
            .annotate(count=Count("id"))
        )

        data["sensor_type_distribution"] = {
            item["sensor_type__name"]: item["count"] for item in sensor_distribution
        }

        return Response(data)
