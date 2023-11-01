from django.shortcuts import render


def homePage(request):
    return render(request, 'core/home.html')


def registerPage(request):
    return render(request, 'core/register.html')


def loginPage(request):
    return render(request, 'core/login.html')

def profilePage(request):
    return render(request, 'core/profile.html')
