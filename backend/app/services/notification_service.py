from sqlalchemy.orm import Session
from ..models.notifications import Notification, NotificationType
from ..models.orders import OrderStatus

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        type: NotificationType,
        title: str,
        message: str
    ):
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message
        )
        db.add(notification)
        db.commit()
        return notification

    @staticmethod
    def create_order_status_notification(db: Session, order, status: OrderStatus):
        status_messages = {
            OrderStatus.CONFIRMED: "Your order has been confirmed",
            OrderStatus.READY: "Your order is ready for pickup",
            OrderStatus.COMPLETED: "Your order has been completed",
            OrderStatus.CANCELLED: "Your order has been cancelled"
        }

        if status in status_messages:
            return NotificationService.create_notification(
                db=db,
                user_id=order.user_id,
                type=NotificationType.ORDER_STATUS,
                title=f"Order #{order.id} Status Update",
                message=status_messages[status]
            ) 