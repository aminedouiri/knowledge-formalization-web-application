from django.shortcuts import render
from apps.connaissance.models import Connaissance
from apps.commentaire.models import Commentaire

# Create your views here.


def notifications(request): 
    connaissances = Connaissance.objects.filter(status_vue=False)
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    commentaires = ""
    if request.user.userprofile.is_expert == False:
        commentaires = Commentaire.objects.all()
        connaissanceNotification += commentaires.count()

    context = {
        'connaissanceNotification': connaissanceNotification,
        'connaissances': connaissances,
        'commentaires': commentaires,
    }

    return render(request, 'notifications/notifications.html', context)
