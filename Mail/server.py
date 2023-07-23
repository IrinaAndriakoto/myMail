from flask import Flask, request, jsonify , render_template , redirect ,url_for
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from flask_mysqldb import MySQL
import mysql.connector
import textdistance
import joblib

app = Flask(__name__)

# mysql = MySQL(app)
config = {
    'user' : 'root',
    'password' : 'root',
    'host' : 'localhost',
    'database' : 'mymail'
    
}


# Charger le modèle de classification binaire et le vecteur "vectorizer" au démarrage du serveur
modele = None
vectorizer = TfidfVectorizer()
api_key_openai = "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"  # Remplacez par votre véritable clé API de OpenAI


connection = mysql.connector.connect(**config)
if connection.is_connected():
    cursor = connection.cursor()
    cursor.execute("SELECT sujet, spam FROM emails")
    rows = cursor.fetchall()
    cursor.close()

# Mettre les données dans un DataFrame pandas
data = pd.DataFrame(rows, columns=['sujet', 'spam'])

# Transformer les colonnes texte (message) en vecteurs numériques
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['sujet'])
y = data['spam']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer et entraîner le modèle de régression logistique
model = LogisticRegression()
model.fit(X_train, y_train)

# Évaluer les performances du modèle
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy du modèle :", accuracy)

# Sauvegarder le modèle dans un fichier
joblib.dump(model, 'modele_spam.pkl')

@app.route('/mettre_a_jour_modele', methods=['GET'])
def mettre_a_jour_modele():
    # Récupérer les données depuis la base de données et préparer les features (X) et la cible (y)
    # ...

    # Entraîner le modèle de régression logistique ou SVM
    # ...

    # Sauvegarder le modèle dans un fichier
    # ...

    return "Modèle mis à jour avec succès !"
# Définir manuellement les mails d'entraînement

# Définir manuellement les étiquettes réelles correspondantes (1 pour SPAM, 0 pour NON SPAM)
# vos_labels = [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1]

# def charger_modele():
#     global modele, vectorizer, api_key_openai
#     # Utiliser vos_donnees_texte et vos_labels définis manuellement
#     X_train = vectorizer.fit_transform(vos_donnees_texte)  # Cela doit être exécuté une seule fois lors de l'entraînement du modèle

#     # Entraîner le modèle de classification binaire en utilisant vos_labels
#     modele = MultinomialNB()
#     modele.fit(X_train, vos_labels)

# # Appeler la fonction pour charger le modèle au démarrage du serveur
# charger_modele()

# Fonction pour effectuer la prédiction de SPAM
# def predict_spam(content):
#     global modele, vectorizer
#     # Convertir le contenu du mail en vecteur de features à l'aide du TfidfVectorizer déjà entraîné
#     content_vector = vectorizer.transform([content])

#     # Effectuer la prédiction en utilisant le modèle chargé
#     prediction = modele.predict(content_vector)[0]

#     # Convertir la prédiction en texte "SPAM" ou "NON SPAM"
#     return "SPAM" if prediction == 1 else "NON SPAM"

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Récupérer les données du corps de la requête POST
#     data = request.get_json()

#     # Récupérer le contenu du mail à prédire
#     content = data['content']

#     # Effectuer la prédiction de SPAM
#     prediction = predict_spam(content)

#     # Retourner le résultat de la prédiction au format JSON
#     result = {'prediction': prediction}
#     return jsonify(result)


@app.route('/')
def boite_de_reception():
    global emails_non_lus
     # Récupérer les e-mails depuis la base de données
    connection = mysql.connector.connect(**config)
    # print("État de mysql.connection :", mysql.connection)
    if connection.is_connected():
        db_info = connection.get_server_info()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM emails where spam=0 limit 6")
        rows = cursor.fetchall()
        
        cursor.close()
    return render_template('boite_de_reception.html',emails_non_lus=rows )

@app.route('/lire_email/<int:email_id>', methods=['POST'])
def marquer_comme_lu(email_id):
    # Mettre à jour l'état "lu" de l'e-mail dans la base de données
    connection = mysql.connector.connect(**config)
    # print("État de mysql.connection :", mysql.connection)
    if connection.is_connected():
        db_info = connection.get_server_info()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM emails")
        rows = cursor.fetchall()
        
    cur =connection.cursor()
    cur.execute("UPDATE emails SET lu = 1 WHERE id = %s", (email_id))
    connection.commit()
    cur.close()

    return redirect('/')


@app.route('/reponse/<int:em>', methods=['GET', 'POST'])
def repondre_email(em):
    # Récupérer les informations de l'e-mail depuis la base de données
    connection = mysql.connector.connect(**config)
    # print("État de mysql.connection :", mysql.connection)
    if connection.is_connected():
        db_info = connection.get_server_info()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM emails where id= %s" , (em,))
        rows = cursor.fetchall()
        
        # email = cursor.fetch()
        cursor.close()

        return render_template('reponse.html', email=rows[0])

@app.route('/')

@app.route('/envoyer_reponse/<int:email_id>', methods=['GET', 'POST'])
def envoyer_reponse(email_id):

        # Récupérer le contenu de la réponse depuis le formulaire POST
        connection = mysql.connector.connect(**config)
        
        contenu_reponse = request.form.get('reponse')
        print(contenu_reponse)
        # Enregistrer la réponse dans la table "reponse"
        cur = connection.cursor()
        cur.execute("INSERT INTO reponse (idMail, content) VALUES (%s, %s)", (email_id, contenu_reponse))
        connection.commit()
        cur.close()

        # Marquer l'e-mail d'origine comme lu dans la table "emails"
        cur = connection.cursor()
        cur.execute("UPDATE emails SET lu = 1 WHERE id = %s", (email_id,))
        connection.commit()
        cur.close()

        cur=connection.cursor()
        cur.execute("select * from reponse where idMail = %s" , (email_id,))
        rows = cur.fetchall()
        cur.close()     
        
        cur=connection.cursor()
        cur.execute("select * from emails where id= %s" , (email_id,) )
        hach = cur.fetchall()
        cur.close()
        
        # return redirect(url_for('boite_de_reception'))
        return render_template('chat.html',email=hach[0] ,reponse=rows)

@app.route('/marquer_comme_spam/<int:email_id>', methods=['POST'])
def marquer_comme_spam(email_id):
    # Mettre à jour l'état "spam" de l'e-mail dans la base de données
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()

        # Update the email's spam status to 1 (True)
        cursor.execute("UPDATE emails SET spam = 1 WHERE id = %s", (email_id,))
        connection.commit()
        cursor.close()
        
        # cursor.execute("insert into spam (idEmail) value (%s) ", (email_id,))
        # connection.commit()
        # cursor.close()

    return redirect('/')

@app.route('/enlever_spam/<int:email_id>', methods=['GET','POST'])
def enlever_spam(email_id):
    # Update the "spam" status of the email in the database
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()
        # Set the "spam" status to 0 (not spam) for the specified email_id
        cursor.execute("UPDATE emails SET spam = 0 WHERE id = %s", (email_id,))
        connection.commit()
        cursor.close()

    return redirect(url_for('afficher_spam'))

@app.route('/spam')
def afficher_spam():
    # Récupérer les e-mails marqués comme spam depuis la base de données
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()

        # Fetch emails marked as spam
        cursor.execute("SELECT * FROM emails WHERE spam = 1")
        spam_emails = cursor.fetchall()
        cursor.close()

    return render_template('spam.html', spam_emails=spam_emails)

@app.route('/get_more_emails/<int:offset>/<int:limit>', methods=['GET'])
def get_more_emails(offset, limit):
    # Récupérer les e-mails supplémentaires depuis la base de données
    # par exemple, en utilisant une requête SQL LIMIT avec OFFSET
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM emails WHERE spam = 0 LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        cursor.close()

    # Générer le code HTML pour les e-mails supplémentaires
    html = ""
    for email in rows:
        html += "<h3>{}</h3>".format(email[1])
        # Ajouter le reste des informations de l'e-mail ici
        # ...
        html += """
        <form action="/reponse/{}" method="post">
            <p><input type="submit" value="Repondre"></p>
        </form>
        """.format(email[0])
    
        # Ajouter le formulaire pour marquer l'e-mail comme spam
        html += """
            <form action="/marquer_comme_spam/{}" method="post">
                <input type="submit" value="Marquer comme spam"> 
            </form>
        """.format(email[0])

    return html

@app.route('/envoyer_message', methods=['POST'])
def envoyer_message():
    # Récupérer les données du formulaire
    destinataire = request.form.get('destinataire')
    message = request.form.get('message')

    # Insérer les données dans la base de données
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (destinataire, message, date) VALUES (%s, %s,NOW())", (destinataire, message))
        connection.commit()
        cursor.close()

    # Rediriger vers la page "sent" pour afficher les messages envoyés
    return redirect('/')

@app.route('/sent')
def sent():
    # Récupérer les messages envoyés depuis la base de données
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages")
        messages = cursor.fetchall()
        cursor.close()

    return render_template('sent.html', messages=messages)

@app.route('/corrector', methods=['POST'])
def corrector():
    if request.method == 'POST':
        word_to_correct = request.form.get('word_to_correct')

        # Récupérer des suggestions de mots basées sur la distance de Damerau
        # Utiliser la fonction closest_word() de la bibliothèque textdistance
        suggestions_damerau = textdistance.closest_word(word_to_correct, list_of_words, n=5)

        return render_template('correction.html', word_to_correct=word_to_correct,  suggestions_damerau=suggestions_damerau)

    return redirect(url_for('boite_de_reception'))

# def inserer_emails_dans_base_de_donnees():
    # # Avant d'appeler cursor()


    # # Insérer les e-mails dans la base de données
    # connection = mysql.connector.connect(**config)
    # # print("État de mysql.connection :", mysql.connection)
    # if connection.is_connected():
    #     db_info = connection.get_server_info()
    #     cursor = connection.cursor()
        
    #     cursor.execute("SELECT * FROM emails")
    #     rows = cursor.fetchall()
        
    #     # print('Sample data  from the table:')
    #     # for row in rows :
    #     #     print(row)


    # # for i, email in enumerate(vos_donnees_texte, start=1):
    # #     cursor.execute("INSERT INTO emails (id, sujet, expediteur, contenu, date, lu) "
    # #                 "VALUES (%s, %s, %s, %s, %s, %s)",
    # #                 ('default', email, email, email, email, email))
    
    # connection.commit()
    # cursor.close()

if __name__ == '__main__':
#     # Insérer les e-mails dans la base de données avant de démarrer l'application Flask
    # inserer_emails_dans_base_de_donnees()

    # Démarrer l'application Flask
    app.run(host='localhost', port=5000)
    
    