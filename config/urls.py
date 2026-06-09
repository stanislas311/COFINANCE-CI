from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from credits.views_dashboard import DashboardAdminView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/credits/', include('credits.urls')),
    path('api/remboursements/', include('remboursements.urls')),
    path('api/assurances/', include('assurances.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/support/', include('support.urls')),
    path('api/dashboard/', DashboardAdminView.as_view(), name='dashboard'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)