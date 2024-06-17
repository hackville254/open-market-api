from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# subject = 'Confirmation de votre achat sur Open Market'
def send_emailB(subject ,username , nom_produit , recipient , url_produit):
    subject = subject
    username = username
    nom_produit = nom_produit
    recipient = recipient
    html_content = render_to_string('email_template.html', {'username': username , 'nom_produit' : nom_produit , 'url_produit':url_produit})
    text_content = strip_tags(html_content)
    # Créer l'email multi alternatives
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True