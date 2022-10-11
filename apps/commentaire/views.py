from django.shortcuts import render, redirect
from apps.connaissance.models import Connaissance
from apps.commentaire.models import Commentaire
import pandas as pd
# Create your views here.

def commente(request, myid):

    connaissance_item = Connaissance.objects.get(id=myid)
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    tableau = ""

    if connaissance_item.forme_connaissance == 'tableau':

        data = pd.read_csv('static/connaissances/'+connaissance_item.url_connaissance)
        tableau = data.to_html()
        
    context = {
        'connaissanceNotification': connaissanceNotification,
        'connaissance_item': connaissance_item,
        'tableau':tableau,
    }

    if 'commente' in request.POST:

        contenu_commentaire = request.POST['commentaire']
        username_expert = request.user.username
        nom_connaissance = connaissance_item.nom_connaissance

        Commentaire(created_for = nom_connaissance, contenu=contenu_commentaire, created_by = username_expert).save()

    if 'cancel' in request.POST:
        return redirect('acceuil')

    return render(request, 'commentaire/commentaire.html', context)