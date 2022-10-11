"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from apps.core.views import home, signup, notFound
from apps.connaissance.views import acceuil, viewi, viewm
from apps.models.views import models, model_element, model_domaine
from apps.notification.views import notifications
from apps.formalisation.views import formalisation
from apps.visualisation.views import visualisation, visualisation_domaine
from apps.commentaire.views import commente

 
admin.site.site_header = 'Administrateur'                   
admin.site.site_title = 'HTML title from adminsitration'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('admin/', admin.site.urls, name='admin'),
    path('404/', notFound, name='notFound'),
    path('acceuil', acceuil, name='acceuil'),
    path('commente/<int:myid>', commente, name='commente'),
    path('acceuil/v/<int:myid>', viewi, name='view'),
    path('models', models, name='models'),
    path('model/<str:mymodele>', model_element, name='model'),
    path('notifications', notifications, name='notifications'),
    path('domaine', model_domaine, name='problem'),
    path('formalisation/view/<int:myid>', viewm, name='viewm'),
    path('formalisation/', formalisation, name='formalisation'),
    path('visualisationi/', visualisation, name='visualisation'),
    path('visualisatione/', visualisation_domaine, name='visualisation_domaine'),
]
