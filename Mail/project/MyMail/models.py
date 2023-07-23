from django.db import models

# Create your models here.
class Email(models.Model):
    sujet = models.CharField(max_length=200)
    contenu = models.TextField()
    expediteur = models.EmailField()
    destinataire = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
class EmailSpam(models.Model):
    text = models.CharField(max_length=200)
    