from abc import ABC, abstractmethod
from typing import Optional, List

class NodeUpdate(ABC):
    @abstractmethod
    def folder_update(self) -> Optional['FolderUpdate']:
        pass

class NodeQuery(ABC):
    pass

class FolderUpdate(ABC):
    @property
    @abstractmethod
    def folder_id(self) -> str:
        pass
