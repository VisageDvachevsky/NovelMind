'''
TODO 

In the future, finalize the permissions system so that co-development can be implemented 
The author of the file (novella) can add user id's to the whitelist and give them permissions
'''

import logging
logging.basicConfig(level=logging.INFO)

class AccessControlManager:
    def __init__(self):
        self.permissions = {}

    def set_permissions(self, user_id: str, permission_type: str) -> None:
        if user_id not in self.permissions:
            self.permissions[user_id] = set()
        self.permissions[user_id].add(permission_type)
        logging.info(f"Permissions set for user {user_id}: {permission_type}")

    def check_permission(self, user_id: str, permission_type: str) -> bool:
        has_permission = permission_type in self.permissions.get(user_id, set())
        logging.info(f"Checking permission for user {user_id}: {permission_type} -> {has_permission}")
        return has_permission

    def set_default_permissions(self, user_id: str) -> None:
        self.set_permissions(user_id, 'read')
        self.set_permissions(user_id, 'write')
        self.set_permissions(user_id, 'delete')
        logging.info(f"Default permissions set for user {user_id}")
