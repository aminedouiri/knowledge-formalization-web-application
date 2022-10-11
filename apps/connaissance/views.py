from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import os, rdflib, pandas as pd
from .models import Connaissance
from apps.commentaire.models import Commentaire
from django.contrib.auth.models import User
from owlready2 import *
from apps.formalisation.views import formalisation

# Create your views here.
def acceuil(request):

    if User.is_authenticated:

        path_folder = 'static/connaissances'
        for x in os.listdir(path_folder):
            if x.endswith('.png'):
                y = x.replace('.png','')
                forms = "image"
            elif x.endswith('.jpg'):
                y = x.replace('.jpg','')
                forms = "image"
            elif x.endswith('.jpeg'):
                y = x.replace('.jpeg','')
                forms = "image"
            elif x.endswith('.pdf'):
                y = x.replace('.pdf','')
                forms = "document"
            elif (x.endswith('.csv') or x.endswith('.xls')):
                y = x.replace('.csv','')
                forms = "tableau"
            try:
                Connaissance.objects.get(nom_connaissance=y)
            except ObjectDoesNotExist:
                Connaissance(nom_connaissance = y, forme_connaissance = forms, url_connaissance = x).save()

        
        connaissance_list = Connaissance.objects.all()
        connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
        if request.user.userprofile.is_expert == False:
            commentaires = Commentaire.objects.all()
            connaissanceNotification += commentaires.count()
        context = {
            'connaissance_list': connaissance_list,
            'connaissanceNotification': connaissanceNotification,
        }


        return render(request, 'connaissances/connaissance.html', context)

    else:
        redirect('login')

def viewi(request, myid):

    connaissance_list = Connaissance.objects.all()
    connaissance_item = Connaissance.objects.get(id=myid)
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    if request.user.userprofile.is_expert == False:
            commentaires = Commentaire.objects.all()
            connaissanceNotification += commentaires.count()
    tableau = ""

    try:
        commentaires = Commentaire.objects.all().filter(created_for = connaissance_item.nom_connaissance)

    except ObjectDoesNotExist:

        commentaires = None

    if connaissance_item.forme_connaissance == 'tableau':

        data = pd.read_csv('static/connaissances/'+connaissance_item.url_connaissance)
        tableau = data.to_html()

    context = {

        'connaissance_list': connaissance_list,
        'connaissance_item': connaissance_item,
        'connaissanceNotification': connaissanceNotification,
        'commentaires': commentaires,
        'tableau':tableau,
    }

    return render(request, 'connaissances/connaissance.html', context)

def viewe(request, myid):

    connaissance_list = Connaissance.objects.all()
    connaissance_item = Connaissance.objects.get(id=myid)
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    tableau = ""

    if connaissance_item.forme_connaissance == 'tableau':

        data = pd.read_csv('static/connaissances/'+connaissance_item.url_connaissance)
        tableau = data.to_html()

        
    context = {
        'connaissance_list': connaissance_list,
        'connaissance_item': connaissance_item,
        'connaissanceNotification': connaissanceNotification,
        'tableau':tableau,
    }

    return render(request, 'connaissances/connaissance.html', context)

def viewm(request, myid):

    formalisation(request)

    connaissance_list = Connaissance.objects.all()
    connaissance_item = Connaissance.objects.get(id=myid)
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    tableau = ""
    if connaissance_item.forme_connaissance == 'tableau':

        data = pd.read_csv('static/connaissances/'+connaissance_item.url_connaissance)
        tableau = data.to_html()
    context = {
        'connaissance_list': connaissance_list,
        'connaissance_item': connaissance_item,
        'connaissanceNotification': connaissanceNotification,
        'tableau':tableau,
    }

    return render(request, 'formalisation/formalisation.html', context)

