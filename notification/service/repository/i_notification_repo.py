from abc import ABCMeta, abstractmethod

from notification.domain.notification import Notification as NotificationVo


class INotificationRepo(metaclass=ABCMeta):
    @abstractmethod
    def save(self, notification_vo: NotificationVo):
        pass
