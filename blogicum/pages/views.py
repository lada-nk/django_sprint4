from django.shortcuts import render


def about(request):
    """Возвращает описание проекта."""
    template_name = 'pages/about.html'
    return render(request, template_name)


def rules(request):
    """Возвращает правила прокта."""
    template_name = 'pages/rules.html'
    return render(request, template_name)
