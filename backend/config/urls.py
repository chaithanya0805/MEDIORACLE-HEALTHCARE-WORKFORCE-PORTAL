from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/facilities/', include('apps.facilities.urls')),
    path('api/professionals/', include('apps.professionals.urls')),
    path('api/shifts/', include('apps.shifts.urls')),
    path('api/matches/', include('apps.matching.urls')),
    path('api/compliance/', include('apps.compliance.urls')),
    path('api/timekeeping/', include('apps.timekeeping.urls')),
    path('api/billing/', include('apps.billing.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
    path('api/support/', include('apps.support.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/audit/', include('apps.audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
