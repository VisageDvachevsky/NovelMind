class AccessControlManager:
    def __init__(self):
        self.permissions = {}

    def set_permissions(self, file_id: str, user_id: str, permission_type: str) -> None:
        if file_id not in self.permissions:
            self.permissions[file_id] = {}
        self.permissions[file_id][user_id] = permission_type

    def check_permission(self, file_id: str, user_id: str, permission_type: str) -> bool:
        return self.permissions.get(file_id, {}).get(user_id) == permission_type