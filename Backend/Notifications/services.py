print("Loading services.py...")
from Config import SessionLocal
from Notifications.models import Notification
print("Imports successful")


def create_notification(docId, deptId, title, message, priority="Normal"):
    db = SessionLocal()

    try:
        notification = Notification(
            docId=docId,
            deptId=deptId,
            title=title,
            message=message,
            priority=priority
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return {
            "message": "Notification created successfully.",
            "notificationId": notification.notificationId
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()


def get_department_notifications(deptId):
    db = SessionLocal()

    try:
        notifications = (
            db.query(Notification)
            .filter(Notification.deptId == deptId)
            .order_by(Notification.createdAt.desc())
            .all()
        )

        return notifications

    finally:
        db.close()

def mark_notification_as_read(notificationId):
    db = SessionLocal()

    try:
        notification = (
            db.query(Notification)
            .filter(Notification.notificationId == notificationId)
            .first()
        )

        if not notification:
            return {"error": "Notification not found."}

        notification.isRead = True

        db.commit()
        db.refresh(notification)

        return {"message": "Notification marked as read."}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()