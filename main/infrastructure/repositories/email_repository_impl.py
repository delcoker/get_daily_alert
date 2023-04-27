import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from main.domain.repositories.email_repository import EmailRepository


class EmailRepositoryImpl(EmailRepository):
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, to_email_list, subject, body):
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = ', '.join(to_email_list)
        message['Subject'] = subject
        message.attach(MIMEText(body))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.email, self.password)
        text = message.as_string()
        server.sendmail(self.email, to_email_list, text)
        server.quit()
