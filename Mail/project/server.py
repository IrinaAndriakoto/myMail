from flask import Flask, request, jsonify , render_template
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Charger le modèle de classification binaire et le vecteur "vectorizer" au démarrage du serveur
modele = None
vectorizer = TfidfVectorizer()
api_key_openai = "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"  # Remplacez par votre véritable clé API de OpenAI

# Définir manuellement les mails d'entraînement
vos_donnees_texte = [
    "Cher client, félicitations, vous avez gagné un voyage gratuit !",
    "Profitez de notre offre spéciale : achetez maintenant et économisez 50% !",
    "Veuillez confirmer vos informations bancaires en cliquant sur le lien ci-dessous.",
    "Gagnez de l'argent rapidement avec notre programme exclusif.",
    "Félicitations, vous avez gagné un iPhone X ! Cliquez pour réclamer votre prix maintenant.",
    "Votre facture est en retard. Veuillez régler le paiement pour éviter des frais supplémentaires.",
    "Invitation spéciale : Économisez 50 sur vos prochains achats pendant 24 heures seulement !",
    "Confirmation de réservation de vol pour votre prochain voyage.",
    "Réclamez votre cadeau gratuit aujourd'hui en participant à notre sondage rapide.",
    "Offre exclusive : Obtenez une réduction de 70 sur tous les produits de beauté.",
    "Urgent : Votre compte bancaire a été compromis, veuillez vérifier vos informations dès maintenant.",
    "Félicitations, vous avez été sélectionné pour une offre d'emploi excitante. Postulez maintenant !",
    "Doublez vos revenus en investissant dans cette opportunité unique.",
    "Avis de livraison en attente pour votre colis. Cliquez pour planifier une nouvelle livraison.",
    "Dernière chance pour acheter notre produit révolutionnaire à prix réduit !",
    "Confirmez votre inscription pour gagner un voyage de luxe à Bali.",
    "Urgent : Gagnez 1000 € par jour en travaillant à domicile.",
    "Mise à jour de sécurité importante : changez votre mot de passe dès maintenant.",
    "Votre compte a été crédité de 500 € en récompense de votre fidélité.",
    "Invitation à un webinaire exclusif sur les investissements immobiliers.",
    "Gagnez une croisière de rêve pour deux en participant à notre tirage au sort.",
    "Réclamez votre échantillon gratuit de notre produit de perte de poids.",
    "Confirmation d'inscription à notre newsletter pour recevoir les meilleures offres.",
    "Investissez dans notre ICO pour devenir riche rapidement !",
    "Votre réservation pour le concert de votre artiste préféré est confirmée.",
    "Boostez votre carrière avec notre formation en ligne de renommée mondiale.",
    "Votre adhésion gratuite à notre club privé a été approuvée.",
    "Ne manquez pas cette offre incroyable pour gagner un voyage tout inclus pour quatre personnes.",
    "Urgent : Votre compte PayPal a été suspendu, veuillez cliquer pour le réactiver.",
    "Vous avez été sélectionné pour participer à un programme de testeur de produits.",
    "Obtenez une réduction de 80 sur notre gamme de produits électroniques.",
    "Confirmation de rendez-vous chez le médecin pour votre examen de santé annuel.",
    "Gagnez un bon d'achat de 1000 € en participant à notre sondage.",
    "Votre paiement a été accepté, merci pour votre achat.",
    "Urgent : Vous avez gagné un iPhone 12 Pro Max. Réclamez votre prix maintenant !",
    "Félicitations, vous avez remporté une croisière gratuite aux Caraïbes.",
    "Planifiez dès maintenant votre escapade de rêve avec nos offres spéciales.",
    "Avis de renouvellement pour votre abonnement à notre plateforme de streaming.",
    "Vous avez été pré-sélectionné pour un prêt sans intérêt. Cliquez pour plus d'informations.",
    "Confirmation de réservation pour votre dîner romantique de la Saint-Valentin.",
    "Obtenez un crédit de 200 € pour chaque ami que vous référez à notre plateforme.",
    "Urgent : Votre compte Amazon a été compromis. Vérifiez vos informations dès maintenant.",
    "Félicitations, vous êtes l'heureux gagnant d'une carte-cadeau de 500 €. Réclamez-la ici.",
    "Planifiez votre prochain voyage avec nos forfaits vacances à prix réduits.",
    "Vous avez été sélectionné pour un essai gratuit de notre logiciel premium.",
    "Obtenez un teint radieux avec notre produit de soin de la peau miracle.",
    "Vous êtes invité à notre soirée de lancement exclusive. Réservez votre place dès maintenant.",
    "Avis de dépassement de votre forfait mobile. Surclassez dès maintenant pour éviter des frais.",
    "Réclamez votre prime de bienvenue en ouvrant un compte bancaire avec nous.",
    "Obtenez un rabais exclusif en utilisant le code SUMMER2023 à la caisse.",
    "Votre inscription à notre programme d'affiliation a été approuvée.",
    "Félicitations, vous avez gagné une carte-cadeau de 100 €. Cliquez pour la réclamer.",
    "Obtenez une remise spéciale de 30 sur tous les articles de mode pour une durée limitée.",
    "Confirmez votre réservation pour l'événement de lancement de notre nouvelle collection.",
    "Gagnez un séjour de luxe à Paris en participant à notre concours exclusif.",
    "Offre spéciale : Achetez un produit, obtenez-en un autre gratuitement.",
    "Profitez de notre vente flash de 24 heures sur tous les produits électroniques.",
    "Confirmez votre présence à notre conférence sur les nouvelles tendances du marché.",
    "Obtenez un crédit de 50 € sur votre prochaine commande en parrainant un ami",
    "Urgent : Votre compte Instagram a été piraté. Cliquez pour récupérer l'accès.",
    "Réservez vos billets pour notre spectacle de danse époustouflant.",
    "Participez à notre sondage pour gagner un bon d'achat de 200 €.",
    "Gagnez un voyage tout inclus aux Maldives en répondant à notre enquête.",
    "Confirmation d'inscription à notre cours en ligne sur le développement personnel.",
    "Obtenez une consultation gratuite avec nos experts en investissement.",
    "Réclamez votre échantillon gratuit de notre nouveau parfum haut de gamme.",
    "Félicitations, vous avez gagné une escapade romantique pour deux. Réservez maintenant !",
    "Vous êtes invité à notre vente privée pour les membres VIP. Profitez de réductions exclusives.",
    "Obtenez une réduction de 40 sur tous les articles de sport pendant notre vente annuelle.",
    "Urgent : Votre compte bancaire a été suspendu. Cliquez pour résoudre le problème.",
    "Participez à notre concours photo pour gagner un appareil photo professionnel.",
    "Obtenez une consultation gratuite avec notre nutritionniste pour atteindre vos objectifs de remise en forme.",
]

# Définir manuellement les étiquettes réelles correspondantes (1 pour SPAM, 0 pour NON SPAM)
vos_labels = [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1]

def charger_modele():
    global modele, vectorizer, api_key_openai
    # Utiliser vos_donnees_texte et vos_labels définis manuellement
    X_train = vectorizer.fit_transform(vos_donnees_texte)  # Cela doit être exécuté une seule fois lors de l'entraînement du modèle

    # Entraîner le modèle de classification binaire en utilisant vos_labels
    modele = MultinomialNB()
    modele.fit(X_train, vos_labels)

# Appeler la fonction pour charger le modèle au démarrage du serveur
charger_modele()

# Fonction pour effectuer la prédiction de SPAM
def predict_spam(content):
    global modele, vectorizer
    # Convertir le contenu du mail en vecteur de features à l'aide du TfidfVectorizer déjà entraîné
    content_vector = vectorizer.transform([content])

    # Effectuer la prédiction en utilisant le modèle chargé
    prediction = modele.predict(content_vector)[0]

    # Convertir la prédiction en texte "SPAM" ou "NON SPAM"
    return "SPAM" if prediction == 1 else "NON SPAM"

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données du corps de la requête POST
    data = request.get_json()

    # Récupérer le contenu du mail à prédire
    content = data['content']

    # Effectuer la prédiction de SPAM
    prediction = predict_spam(content)

    # Retourner le résultat de la prédiction au format JSON
    result = {'prediction': prediction}
    return jsonify(result)

def boite_de_reception():
    emails_non_lus = [
        {'sujet': "Cher client, félicitations, vous avez gagné un voyage gratuit !", 'expediteur': "spam@example.com", 'contenu': "Contenu du spam", 'date': "2023-07-20"},
        {'sujet': "Votre compte a été crédité de 500 € en récompense de votre fidélité.", 'expediteur': "amis@example.com", 'contenu': "Contenu du message important", 'date': "2023-07-20"},
    ]
    
    return render_template('accueil.php', emails_non_lus=emails_non_lus)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
    