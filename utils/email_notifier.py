import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pandas.io.formats.format import return_docstring
from pandas.io.formats.info import frame_see_also_sub

def send_email(smtp_server, port, login, password, sender_email, receiver_email, subject, body):
    try:
        # Create the email headers and body
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
    return False

# Example usage:
if __name__ == "__main__":
    smtp_server = "smtp.example.com"
    port = 587
    login = "youremail@gmail.com",
    password= "yourpassword",
    sender_email= "sender_email@gmail.com",
    receiver_email = "receiver_email_@gmail.com"
    subject= "Test Email",
    body= "This is a test email sent from the email_notifier module.",

success = send_email(
    smtp_server, port, login, password,
    sender_email, receiver_email,
    subject, body
)
if success:
    print("Email sent successfully.")
else:
    print("Failed to send email.")
