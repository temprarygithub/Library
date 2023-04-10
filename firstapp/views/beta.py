from django.shortcuts import render

def view_c(request):
    return render(request, 'view_c.html')

def view_d(request):
    return render(request, 'view_d.html')