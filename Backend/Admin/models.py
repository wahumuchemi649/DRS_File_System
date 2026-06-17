from Auth.models import User
from Config import Base

class Admin(User):

    __mapper_args__ ={
        "polymorphic_identity":"Admin"
    }
    def get_permissions(self):
        return[
            "create_user",
            "delete_user",
            "update_user",
            "view_user",
            "manage_departments",
            "manage_files",
            "manage_access_requests",
            "view_audit_logs",
            "manage_system_settings",
            "view_reports",
            "change_status"
        ]
    def check_privilege(self, privilege_name: str) -> bool:
        """Helper to quickly verify if an admin can perform an action."""
        return privilege_name.upper() in self.get_permissions()
    