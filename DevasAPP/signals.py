import threading
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from .models import Order


from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_delievered_email(order):
    subject = f"Your Order #{order.id} Has Been Delivered Successfully"
    html_content = render_to_string(
        "emails/order_deliverd.html",
        {
            "order": order,
            "name": f"{order.first_name} {order.last_name}",
            "order_id": order.id,
            "email": order.email,
            "phone": order.phone,
            "items": order.items.all()
        }
    )

    email = EmailMultiAlternatives(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

   


def on_way_email(order):
    subject = f"Your Order #{order.id} Has Been Shipped"
    html_content = render_to_string(
        "emails/on_the_way_notification.html",
        {
            "order": order,
            "name": f"{order.first_name} {order.last_name}",
            "order_id": order.id,
            "email": order.email,
            "phone": order.phone,
            "items": order.items.all()
        }
    )

    email = EmailMultiAlternatives(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()



@receiver(pre_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):

    if not instance.pk:
        return

    try:
        old_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    # if status changed
    if old_order.status != instance.status:

        subject = ""
        message = ""


        if instance.status == "on_the_way":

            print(f"Order #{instance.id} status changed to 'on_the_way'. Sending email to {instance.email}...")
          

            thread = threading.Thread(
                    target=on_way_email,
                    args=(instance,)
                )
            thread.start()

        elif instance.status == "delivered":
            
            thread = threading.Thread(
                target=send_delievered_email,
                args=(instance,)
            )
            thread.start()