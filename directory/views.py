from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from django.db.models import Q
from core.models import UserProfile


def widget_view(request):
    query = request.GET.get('search', '').lower()

    profiles = UserProfile.objects.select_related('user', 'department')

    if query:
        profiles = profiles.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(department__name__icontains=query)
        )

    profiles = profiles.order_by('user__last_name')
    paginator = Paginator(profiles, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('directory/_widget_results.html', {
            'page_obj': page_obj,
            'search': query
        })
        return JsonResponse({'html': html})

    return render(request, 'directory/widget.html', {
        'page_obj': page_obj,
        'search': query
    })
