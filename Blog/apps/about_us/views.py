from django.shortcuts import render

# Create your views here.
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