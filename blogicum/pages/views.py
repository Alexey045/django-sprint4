from django.shortcuts import render


def csrf_failure(request, reason=""):
    return render(request, "pages/403csrf.html", status=403)


def page_403(request, exception=None):
    return render(request, "pages/403csrf.html", status=403)


def page_404(request, exception=None):
    return render(request, "pages/404.html", status=404)


def page_500(request):
    return render(request, "pages/500.html", status=500)
