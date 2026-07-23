from flask import Blueprint, jsonify, request
from Notifications.services import (
    create_notification,
    get_department_notifications,
    mark_notification_as_read
)

Notification_bp = Blueprint("Notification", __name__)


@Notification_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Notification module is working."})


@Notification_bp.route("/create", methods=["POST"])
def create():

    data = request.get_json()

    result = create_notification(
        docId=data["docId"],
        deptId=data["deptId"],
        title=data["title"],
        message=data["message"],
        priority=data.get("priority", "Normal")
    )

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@Notification_bp.route("/<deptId>", methods=["GET"])
def get_notifications(deptId):

    notifications = get_department_notifications(deptId)

    results = []

    for n in notifications:
        results.append({
            "notificationId": n.notificationId,
            "title": n.title,
            "message": n.message,
            "priority": n.priority,
            "isRead": n.isRead,
            "createdAt": str(n.createdAt)
        })

    return jsonify(results), 200

@Notification_bp.route("/read/<int:notificationId>", methods=["PUT"])
def mark_read(notificationId):

    result = mark_notification_as_read(notificationId)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200