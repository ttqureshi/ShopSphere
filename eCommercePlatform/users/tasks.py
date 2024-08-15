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
            summary += f"Total Amount: {order.total_price}\n"
            summary += "------------------------------\n"
    mail_subject = "Daily Orders Summary"

    send_mail(
        subject=mail_subject,
        message=summary,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )
