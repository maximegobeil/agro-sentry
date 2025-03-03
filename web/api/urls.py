from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    CustomTokenObtainPairView,
    LogoutView,
    OrganizationMembershipViewSet,
    OrganizationStatsViewSet,
    OrganizationViewSet,
)

router = DefaultRouter()
router.register(r"organizations", OrganizationViewSet, basename="organization")


urlpatterns = [
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path(
        "organizations/<int:pk>/members/",
        OrganizationMembershipViewSet.as_view({"get": "list"}),
        name="organization-members",
    ),
    path(
        "organizations/<int:pk>/stats/",
        OrganizationStatsViewSet.as_view({"get": "retrieve"}),
        name="organization-stats",
    ),
    *router.urls,
]
