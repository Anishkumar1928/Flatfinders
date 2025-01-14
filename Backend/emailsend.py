import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email(recipient_email, subject, body):
    sender_email=os.getenv("SENDER_EMAIL")
    sender_password="pfvkohspulwawdik"
    try:
        html_file_path = "./templates/mail.html"
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_template = file.read()
        html_content = html_template.replace("123456", body)
        # Create the message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

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
#     recipient_email="mr.anish.kmr@gmail.com",
#     subject="Test Email",
#     body="This is a test email sent using smtplib!"
# )
