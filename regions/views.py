from django.shortcuts import render
from core.models import Region

def region_list(request):
    regions = Region.objects.select_related('manager').prefetch_related('branches').all()
    return render(request, 'regions/region_list.html', {'regions': regions})
