from django.db import DatabaseError

from notification.domain.notification import Notification as NotificationVo
from notification.infra.serializer import NotificationSerializer
from notification.service.repository.i_notification_repo import INotificationRepo


class NotificationRepo(INotificationRepo):
    def save(self, notification_vo: NotificationVo):
        dicted = notification_vo.to_dict()
        serializer = NotificationSerializer(data=dicted)
        if serializer.is_valid():
            serializer.save()
            return notification_vo
        else:
            raise DatabaseError(serializer.errors)
