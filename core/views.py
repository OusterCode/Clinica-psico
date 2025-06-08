from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    return render(request, 'index.html')

@login_required
def welcome(request):
    return render(request, 'welcome.html')
