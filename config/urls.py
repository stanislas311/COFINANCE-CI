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
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('credits_view/', TemplateView.as_view(template_name='credits.html'), name='credits_view'),
    path('remboursements_view/', TemplateView.as_view(template_name='remboursements.html'), name='remboursements_view'),
    path('assurances_view/', TemplateView.as_view(template_name='assurances.html'), name='assurances_view'),
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)