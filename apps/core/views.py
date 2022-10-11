from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CreationUserForm

from apps.userprofile.models import Userprofile
from apps.connaissance.models import Connaissance

# Create your views here.
def home(request):
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()

    context = {
        'connaissanceNotification': connaissanceNotification,
    }

    if request.user.is_authenticated: 
        return redirect('acceuil')
        

    return render(request, 'core/home.html', context)
    
def signup(request):
    if request.method == 'POST':
        form = CreationUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            account_type = request.POST.get('account_type', 'ingenieur')

            if account_type == 'expert':
                userprofile = Userprofile.objects.create(user=user, is_expert=True)
                
            else:
                userprofile = Userprofile.objects.create(user=user)
                
            userprofile.save()
            login(request, user)

            return redirect('acceuil')
            
    else:
        form = CreationUserForm()

    return render(request, 'core/signup.html', {'form': form})

def services(request):
    
    return render(request, 'core/services.html')

def notFound(request):
    return render(request, 'core/notFound.html')