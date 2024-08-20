from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def send_daily_order_summary():
    from .models import Order

    yesterday = now() - timedelta(days=1)
    orders = Order.objects.filter(order_date__gte=yesterday)
    if not orders.exists():
        summary = "No new orders in the last 24 hours"
    else:
        summary = "Daily Order Summary\n\n"
        for order in orders:
            summary += f"Order ID: {order.id}\n"
            summary += f"Customer Name: {order.full_name}\n"
            for order_item in order.orderitem_set.all():
                summary += f"\tItem: {order_item.product.name}\n\t"
                summary += f"Unit Price: Rs. {order_item.product.price}\n\t"
                summary += f"Quantity: {order_item.quantity}\n\n"
            summary += f"Total Amount: Rs. {order_item.total_price}\n"
            summary += "------------------------------\n"
    mail_subject = "Daily Orders Summary"

    send_mail(
        subject=mail_subject,
        message=summary,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )


@shared_task
def send_sms(order_id):
    from twilio.rest import Client
    from .models import Order

    order = Order.objects.get(id=order_id)
    order_items = order.orderitem_set.all()
    order_summary = "ORDER DETAILS\n\nProduct \t\tQuantity\t\tTotal Price\n"
    for item in order_items:
        order_summary += (
            f"{item.product.name} \t{item.quantity} \t Rs.{item.total_price}\n"
        )

    order_summary += f"\nTotal Bill: Rs. {order.total_price}"

    client = Client(settings.ACCOUNT_SSID, settings.AUTH_TOKEN)
    message = client.messages.create(
        from_=settings.TWILIO_NUMBER, body=order_summary, to=settings.SEND_SMS_TO
    )
