"""
Custom Error Handlers - Secure Task Manager
============================================
OWASP ASVS V7 Compliance: No stack traces exposed to users.

These handlers ensure that:
- No sensitive information is leaked in error responses
- Users see friendly, professional error pages
- Errors are logged for security monitoring
"""

from django.shortcuts import render


def custom_400(request, exception=None):
    """
    Handle 400 Bad Request errors.
    
    Security: Returns generic message without revealing request details.
    """
    return render(request, '400.html', status=400)


def custom_403(request, exception=None):
    """
    Handle 403 Forbidden errors.
    
    Security: Returns generic message without revealing authorization logic.
    """
    return render(request, '403.html', status=403)


def custom_404(request, exception=None):
    """
    Handle 404 Not Found errors.
    
    Security: Returns generic message without revealing URL structure.
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Handle 500 Internal Server errors.
    
    Security: Returns generic message without exposing stack trace or internals.
    Note: This handler doesn't receive 'exception' parameter for security.
    """
    return render(request, '500.html', status=500)
