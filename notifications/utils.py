from .models import Notification


def creer_notification(destinataire, titre, message, type_notif='general'):
    return Notification.objects.create(
        destinataire=destinataire,
        titre=titre,
        message=message,
        type_notif=type_notif,
    )