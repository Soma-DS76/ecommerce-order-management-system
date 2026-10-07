import smtplib
from email.message import EmailMessage
import os

from dotenv import load_dotenv

load_dotenv()


def send_order_email(
    customer_email: str,
    order_number: str,
    grand_total: str
):
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM')

    print('SMTP HOST:', smtp_host)
    print('SMTP PORT:', smtp_port)
    print('SMTP USER:', smtp_user)
    print('PASSWORD LOADED:', bool(smtp_password))
    print('SMTP FROM:', smtp_from)

    message = EmailMessage()
    message['Subject'] = 'Order Confirmation'
    message['From'] = smtp_from
    message['To'] = customer_email

    message.set_content(
        f'''Your order has been placed successfully.

Order Number: {order_number}
Total Amount: ₹{grand_total}

Thank you for your order.
'''
    )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)


def send_order_status_email(
    customer_email: str,
    order_number: str,
    order_status: str
):
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM')

    print('STATUS EMAIL STARTED')
    print('SMTP HOST:', smtp_host)
    print('SMTP PORT:', smtp_port)
    print('SMTP USER:', smtp_user)
    print('PASSWORD LOADED:', bool(smtp_password))
    print('SMTP FROM:', smtp_from)
    print('CUSTOMER EMAIL:', customer_email)
    print('ORDER NUMBER:', order_number)
    print('ORDER STATUS:', order_status)

    message = EmailMessage()
    message['Subject'] = 'Order Status Update'
    message['From'] = smtp_from
    message['To'] = customer_email

    message.set_content(
        f'''Your order status has been updated.

Order Number: {order_number}
Current Status: {order_status}

Thank you for shopping with us.
'''
    )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    print('STATUS EMAIL SENT')