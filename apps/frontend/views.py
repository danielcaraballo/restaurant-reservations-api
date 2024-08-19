from django.shortcuts import render

def inicio(request, exception=None):
    return render(request, "inicio/inicio.html", {})

def bad_request(request, exception=None):
    return render(request, "errores/400.html", {})

def permission_denied(request, exception=None):
    return render(request, "errores/403.html", {})

def page_not_found(request, exception):
    return render(request, "errores/404.html", {})

def server_error(request, exception=None):
    return render(request, "errores/500.html", {})