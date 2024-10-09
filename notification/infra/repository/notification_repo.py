from django.contrib.contenttypes.models import ContentType
from django.db import DatabaseError

from notification.domain.notification import Notification as NotificationVo
from notification.infra.models import Notification
from notification.infra.serializer import NotificationSerializer
from notification.service.repository.i_notification_repo import INotificationRepo


class NotificationRepo(INotificationRepo):
    def save(self, notification_vo: NotificationVo):
        dicted = notification_vo.to_dict()
        # 시리얼라이저에 데이터 전달
        serializer = NotificationSerializer(data=dicted)

        # 유효성 검사 및 저장
        if serializer.is_valid():
            serializer.save()
            return notification_vo
        else:
            raise DatabaseError(serializer.errors)
