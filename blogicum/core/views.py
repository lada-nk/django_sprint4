from django.shortcuts import render


def page_not_found(request, exception):
    """Обработка ошибки 404"""
    return render(request, 'core/404.html', status=404)


def csrf_failure(request, reason=''):
    """Обработка ошибки 403"""
    return render(request, 'core/403csrf.html', status=403) 


def server_failure(request, exception):
    """Обработка ошибки 500"""
    return render(request, 'core/500.html', status=500) 