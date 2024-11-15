from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(order):
    subject = 'Order Confirmation'
    message = (
        f"Dear {order.user.username},\n\n"
        f"Thank you for your order #{order.id}! Your order has been successfully placed.\n\n"
        f"Order Details:\nTotal Price: ${order.total_price}\n\n"
        "We will notify you once your order ships.\n\n"
        "Best Regards,\nWatch Store Team"
    )
    
    recipient_list = [order.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
