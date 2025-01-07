import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email="flatfindersapp@gmail.com"
sender_password="Anishkumar8084"

def send_email(recipient_email, subject, body):
    try:
        # Create the message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable TLS
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# # Example usage
# send_email(
#     sender_email="your_email@gmail.com",
#     sender_password="your_app_password",  # Use App Password here
#     recipient_email="recipient_email@gmail.com",
#     subject="Test Email",
#     body="This is a test email sent using smtplib!"
# )