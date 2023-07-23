<!DOCTYPE html>
<html>
<head>
    <title>Classification des mails</title>
    {% comment %} <link rel="stylesheet" href="../assets/style.css"> {% endcomment %}
</head>
<body style="text-align:center">
    <div class="header">
        MyMail
    </div>
    {% comment %} <div class="content">
        <h1>Classification des mails</h1>
        <form action="../inc/traitement.php" method="post">
            <label for="mail_content">Contenu du mail:</label><br>
            <textarea id="mail_content" name="mail_content" rows="5" cols="50"></textarea><br>
            <input type="submit" value="Classer">
        </form>
    </div> {% endcomment %}
    <h1>Boite de réception</h1>
        {% for email in emails_non_lus %}
            <h2>{{ email.sujet }}</h2>
            <p>{{ email.expediteur }}</p>
            <p>{{ email.contenu }}</p>
            <p>{{ email.date }}</p>
            <a href="/lire_email/{{ email.id }}">Lire</a> <br>
            <hr>
        {% endfor %}>

    <h1>Envoyer un Mail </h1>
        <textarea> </textarea> <br>
        <input type="text"> <br> <br>
        <input type="submit" value="Envoyer">

    <h1>Spam</h1>

</body>
</html>