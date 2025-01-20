import resend
from django.conf import settings
from django.template.loader import render_to_string

class EmailService:
    @staticmethod
    def initialize():
        resend.api_key = settings.RESEND_API_KEY

    @staticmethod
    def send_verification_email(user_email, verification_url):
        try:
            # Charger le template HTML
            html_content = render_to_string('emails/verify_email.html', {
                'verification_url': verification_url
            })

            params = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": user_email,
                "subject": "Vérifiez votre adresse email",
                "html": html_content
            }
            
            response = resend.Emails.send(params)
            return response
        except Exception as e:
            print(f"Erreur d'envoi d'email: {str(e)}")
            raise

    @staticmethod
    def send_password_reset_email(user_email, reset_url):
        try:
            html_content = render_to_string('emails/reset_password.html', {
                'reset_url': reset_url
            })

            params = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": user_email,
                "subject": "Réinitialisation de votre mot de passe",
                "html": html_content
            }
            
            response = resend.Emails.send(params)
            return response
        except Exception as e:
            print(f"Erreur d'envoi d'email: {str(e)}")
            raise