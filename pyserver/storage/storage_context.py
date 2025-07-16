from pyserver.storage.node_storage import NodeStorage
from pyserver.storage.edge_storage import EdgeStorage
from pyserver.storage.settings_storage import SettingsStorage
from pyserver.storage.file_storage import FileStorage
from pyserver.storage.user.user_storage import UserStorage
from pyserver.storage.folder_storage import FolderStorage
from pyserver.storage.index.tracker import FolderTracker

class StorageContext:
    def __init__(self, user_id: str):
        """
        Central storage context for managing all database connections and storage operations.
        
        Args:
            user_id: The user ID for this storage context
        """
        self.user_id = user_id
        self.node_storage = NodeStorage(user_id)
        self.edge_storage = EdgeStorage(user_id)
        self.settings_storage = SettingsStorage(user_id)
        self.file_storage = FileStorage(user_id)
        self.user_storage = UserStorage()
        self.folder_storage = FolderStorage(user_id)
        self.folder_tracker = FolderTracker(self.user_id)

    def node_storage(self) -> NodeStorage:
        """Get the node storage instance."""
        return self.node_storage

    def edge_storage(self) -> EdgeStorage:
        """Get the edge storage instance."""
        return self.edge_storage

    def folder_storage(self) -> FolderStorage:
        """Get the folder storage instance."""
        return self.folder_storage

    def settings_storage(self) -> SettingsStorage:
        """Get the settings storage instance."""
        return self.settings_storage

    def file_storage(self) -> FileStorage:
        """Get the file storage instance."""
        return self.file_storage

    def user_storage(self) -> UserStorage:
        """Get the user storage instance."""
        return self.user_storage

    def folder_tracker(self) -> FolderTracker:
        """Get the folder tracker instance."""
        return self.folder_tracker
