from django.urls import path
from .views import (
    asset_list,
    asset_create,
    asset_detail,
    asset_update,
    asset_dashboard,
    no_access,
)

urlpatterns = [
    path("", asset_list, name="asset-list"),
    path("dashboard/", asset_dashboard, name="asset-dashboard"),
    path("create/", asset_create, name="asset-create"),
    path("<int:pk>/", asset_detail, name="asset-detail"),
    path("<int:pk>/edit/", asset_update, name="asset-edit"),
    path("no-access/", no_access, name="no-access"),
]
