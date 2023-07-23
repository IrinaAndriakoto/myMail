from django.shortcuts import render
from MyMail.models import Email

# Create your views here.

def accueil(request):
    emails_non_lus = Email.objects.filter(lu=False)
    context = {'emails_non_lus': emails_non_lus}
    return render(request, 'accueil.php', context)