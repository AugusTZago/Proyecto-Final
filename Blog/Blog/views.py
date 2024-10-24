from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def acerca_de(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def contacto(request):
    return render(request, 'contact.html')

def post(request):
    return render(request, 'post-details.html')

def registrar(request):
    return render(request, 'register.html')

