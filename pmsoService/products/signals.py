from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Q
from .models import Product, ProductOrder
from notifications.models import Notification
from account.models import User

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    actor = kwargs.get('user')  # Expecting the user to be passed in kwargs
    changes = instance.get_changes()

    create_notifications_for_product(instance, action, actor, changes)

def create_notifications_for_product(product, action, actor=None, changes=None):
    admin_users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    
    changes_message = f"\nThese are the changes: {', '.join(changes)}." if changes else ""
    
    for user in admin_users:
        message = (
            f'Product "{product.name}" has been {action} by '
            f'"{actor.display_name if actor and actor.display_name else actor.username if actor else "an unknown user"}"{changes_message}'
        )
        Notification.objects.create(
            product=product,
            message=message,
            user=user,
            action=action,  # Add action field to the notification
            actor=actor
        )

@receiver(post_save, sender=ProductOrder)
def product_order_saved(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    actor = kwargs.get('user')  # Expecting the user to be passed in kwargs
    changes = instance.get_changes()

    create_notifications_for_product_order(instance, action, actor, changes)

def create_notifications_for_product_order(order, action, actor=None, changes=None):
    users_to_notify = set()

    if order.sale_staff:
        users_to_notify.add(order.sale_staff)  # Notify sale staff
    admin_users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    users_to_notify.update(admin_users)  # Notify all admin users

    changes_message = f"\nThese are the changes: {', '.join(changes)}." if changes else ""

    for user in users_to_notify:
        message = (
            f'Product Order "{order.name}" has been {action} by '
            f'"{actor.display_name if actor and actor.display_name else actor.username if actor else "an unknown user"}"{changes_message}'
        )
        Notification.objects.create(
            product_order=order,
            message=message,
            user=user,
            action=action,  # Add action field to the notification
            actor=actor
        )
