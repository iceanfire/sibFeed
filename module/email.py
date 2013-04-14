from google.appengine.api import mail

def sendAnswerNotification():
    pass


def sendNotification(email,subject,message):
        emailAddress = email

        if not mail.is_email_valid(emailAddress):
            return False

        else:
            sendAddress = "Learn To Do <admin@learntodo.co>"
            body = message
            return mail.send_mail(sendAddress, emailAddress, subject, body)