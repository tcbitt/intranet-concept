from django.contrib import admin
from .models import AssetType, Brand, ModelType, Asset, Status


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(ModelType)
class ModelTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'created_at', 'updated_at')
    search_fields = ('name', 'brand__name')
    list_filter = ('brand',)
    ordering = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'asset_type',
        'model_type',
        'checked_out_to_user',
        'checked_out_to_branch',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'checked_out_to_user__username', 'checked_out_to_branch__name')
    list_filter = ('asset_type', 'model_type', 'checked_out_to_branch')
    ordering = ('-updated_at',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'color', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)