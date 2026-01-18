from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from tasks.views import RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tasks/', include('tasks.urls')),
]

# =============================================================================
# DEBUG-ONLY TEST ENDPOINTS (automatically disabled when DEBUG=False)
# =============================================================================
if settings.DEBUG:
    def test_400(request):
        from django.core.exceptions import SuspiciousOperation
        raise SuspiciousOperation("Test 400 error")

    def test_403(request):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Test 403 error")

    def test_500(request):
        raise Exception("Test 500 error")

    urlpatterns += [
        path('test-400/', test_400, name='test_400'),
        path('test-403/', test_403, name='test_403'),
        path('test-500/', test_500, name='test_500'),
    ]

# =============================================================================
# CUSTOM ERROR HANDLERS (OWASP ASVS V7 - No Stack Traces Exposed)
# =============================================================================
handler400 = 'securetaskapp.views.custom_400'
handler403 = 'securetaskapp.views.custom_403'
handler404 = 'securetaskapp.views.custom_404'
handler500 = 'securetaskapp.views.custom_500'
