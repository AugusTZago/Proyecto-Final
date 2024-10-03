from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'templates/index.html')

def acerca_de(request):
    return render(request, 'templates/about.html')

def blog(request):
    return render(request, 'templates/blog.html')

def contacto(request):
    return render(request, 'templates/contact.html')

def post(request):
    return render(request, 'templates/post-details.html')