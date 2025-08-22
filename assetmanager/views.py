from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from accesscontrol.decorators import role_required
from .models import Asset, AssetType, ModelType, Status
from .forms import AssetForm


@role_required('Support')
def asset_list(request):
    search_query = request.GET.get('search', '')
    asset_type_filter = request.GET.get('asset_type')
    model_type_filter = request.GET.get('model_type')
    status_type_filter = request.GET.get('status_type')

    assets = Asset.objects.select_related(
        'asset_type', 'model_type', 'checked_out_to_user', 'checked_out_to_branch'
    ).order_by('-updated_at')

    if search_query:
        assets = assets.filter(
            Q(name__icontains=search_query) |
            Q(model_type__name__icontains=search_query) |
            Q(checked_out_to_user__username__icontains=search_query) |
            Q(checked_out_to_user__first_name__icontains=search_query) |
            Q(checked_out_to_user__last_name__icontains=search_query) |
            Q(checked_out_to_branch__name__icontains=search_query)
        )

    if asset_type_filter:
        assets = assets.filter(asset_type__id=asset_type_filter)

    if model_type_filter:
        assets = assets.filter(model_type__id=model_type_filter)

    if status_type_filter:
        assets = assets.filter(status_type__id=status_type_filter)

    paginator = Paginator(assets, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search_query,
        'asset_types': AssetType.objects.all(),
        'model_types': ModelType.objects.all(),
        'status_types': Status.objects.all(),
        'selected_asset_type': asset_type_filter,
        'selected_model_type': model_type_filter,
        'selected_status_type': status_type_filter,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('assetmanager/_asset_results.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'assetmanager/asset_list.html', context)


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
