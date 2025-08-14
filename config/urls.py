from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('directory/', include('directory.urls')),
    path('documents/', include('documents.urls')),
    path('hr/', include('human_resources.urls')),
    path('helpdesk/', include('helpdesk.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
