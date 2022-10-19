from flask import current_app, render_template
from flask_mail import Message


def send_mail(subject,sender,recipients,html_body):
    msg = Message(subject,sender=sender,recipients=recipients)
    #msg.body = text_body
    msg.html = html_body
    with current_app.app_context():
        mail.send(msg)

def mail_for_reset_password(user):
    token = user.get_reset_password_token()
    send_mail('change password',current_app.config['ADMINS'][0],[user.email],
        render_template('mail/message_for_reset_password.html',token=token,user=user))










