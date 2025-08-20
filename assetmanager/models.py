from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Asset Type"
        verbose_name_plural = "Asset Types"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

class ModelType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brand')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Model Type"

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=100)
    asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT, related_name='assets')
    model_type = models.ForeignKey(ModelType, on_delete=models.PROTECT, related_name='models')
    status_type = models.ForeignKey(Status, on_delete=models.PROTECT, default=1, related_name='status')
    checked_out_to_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='checked_out_assets'
    )
    checked_out_to_branch = models.ForeignKey(
        'core.Branch',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='branch_assets'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.checked_out_to_user and not self.checked_out_to_branch:
            raise ValidationError("Asset must be checked out to either a user or a branch.")
        if self.checked_out_to_user and self.checked_out_to_branch:
            raise ValidationError("Asset cannot be checked out to both a user and a branch.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name