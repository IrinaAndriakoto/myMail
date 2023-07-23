from django.urls import path
from MyMail import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    # path('    ')
    # Ajoutez d'autres URL pour les vues supplémentaires
]