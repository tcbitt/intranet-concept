from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from accesscontrol.decorators import role_required
from .models import Asset
from .forms import AssetForm  # You’ll need to create this

@role_required('Support')
def asset_list(request):
    assets = Asset.objects.select_related(
        'asset_type', 'model_type', 'checked_out_to_user', 'checked_out_to_branch'
    ).order_by('-updated_at')

    paginator = Paginator(assets, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'assetmanager/asset_list.html', {'assets': page_obj})


@role_required('Support')
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            return redirect('asset-list')
    else:
        form = AssetForm()

    return render(request, 'assetmanager/asset_form.html', {'form': form})


@role_required('Support')
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    return render(request, 'assetmanager/asset_detail.html', {'asset': asset})


@role_required('Support')
def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset-detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)

    return render(request, 'assetmanager/asset_form.html', {'form': form, 'asset': asset})


@role_required('Support')
def asset_dashboard(request):
    context = {}

    context['recent_assets'] = Asset.objects.order_by('-created_at')[:10]

    context['checked_out_assets'] = Asset.objects.filter(
        models.Q(checked_out_to_user__isnull=False) | models.Q(checked_out_to_branch__isnull=False)
    )

    context['available_assets'] = Asset.objects.filter(
        checked_out_to_user__isnull=True,
        checked_out_to_branch__isnull=True
    )

    context['asset_type_counts'] = Asset.objects.values('asset_type__name').annotate(count=models.Count('id'))

    return render(request, 'assetmanager/dashboard.html', context)

def no_access(request):
    return render(request, 'core/no_access.html')
