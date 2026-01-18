from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from tasks.views import RegisterView


# Test views for error pages (remove in production)
def test_400(request):
    from django.core.exceptions import SuspiciousOperation
    raise SuspiciousOperation("Test 400 error")

def test_403(request):
    from django.core.exceptions import PermissionDenied
    raise PermissionDenied("Test 403 error")

def test_500(request):
    raise Exception("Test 500 error")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tasks/', include('tasks.urls')),
    # Test error pages (remove in production)
    path('test-400/', test_400, name='test_400'),
    path('test-403/', test_403, name='test_403'),
    path('test-500/', test_500, name='test_500'),
]
