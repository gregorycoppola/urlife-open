import logging
import uuid
from typing import List
from pyserver.storage.storage_context import StorageContext
from pyserver.storage.node_storage import NodeStorage
from pyserver.system.graph_node import GraphNode, ParentRef
from fastapi import APIRouter, Depends, HTTPException

logger = logging.getLogger(__name__)

class FolderNames:
    ROOT_ID = "User"
    # Root
    USER = "User"
    
    # Journal
    INBOX = "Inbox"
    JOURNAL = "Journal"
    
    # Unsorted
    PROJECTS = "Projects"
    
    # Business
    BUSINESS = "Business"
    PRODUCT = "Product"
    HOME = "Home"
    LIFE = "Life"
    MONEY = "Money"
    BODY = "Body"
    SOCIAL = "Social"
    
    # Social
    PEOPLE = "People"

def root_node_id() -> str:
    return FolderNames.ROOT_ID

class SetupFolder:
    def __init__(self, name: str, children: List['SetupFolder'] = None):
        self.name = name
        self.children = children or []

def root_folder_name() -> str:
    return FolderNames.USER

def inbox_folder_name() -> str:
    return FolderNames.INBOX

def journal_folder_name() -> str:
    return FolderNames.JOURNAL

def projects_folder_name() -> str:
    return FolderNames.PROJECTS

def people_folder_name() -> str:
    return FolderNames.PEOPLE

def get_standard_setup() -> SetupFolder:
    return SetupFolder(
        name=root_folder_name(),
        children=[
            SetupFolder(name=inbox_folder_name()),
            SetupFolder(name=journal_folder_name()),
            SetupFolder(
                name=projects_folder_name(),
                children=[
                    SetupFolder(name=FolderNames.BUSINESS),
                    SetupFolder(name=FolderNames.PRODUCT),
                    SetupFolder(name=FolderNames.HOME),
                    SetupFolder(name=FolderNames.MONEY),
                    SetupFolder(name=FolderNames.LIFE),
                    SetupFolder(name=FolderNames.BODY),
                    SetupFolder(name=FolderNames.SOCIAL),
                ]
            ),
            SetupFolder(name=people_folder_name()),
        ]
    )

async def recursively_make_children(
    storage: StorageContext,
    current: SetupFolder,
    parent: GraphNode
) -> None:
    """Create child nodes recursively and register in folder index."""
    try:
        for child_spec in current.children:
            logger.info(f"Creating child node: {child_spec.name}")
            node_id = str(uuid.uuid4())
            child_node = GraphNode(
                node_id=node_id,
                object_type="FOLDER",
                caption=child_spec.name,
                extra_properties={"entry_method": "SYSTEM"},
                parent=ParentRef(edge_label="CHILD_OF", parent_id=parent.node_id)
            )

            await storage.node_storage.store_node(child_node)
            await storage.folder_tracker.add_to_folder(parent.node_id, child_node.node_id)

            await recursively_make_children(storage, child_spec, child_node)
    except Exception as e:
        logger.error(f"Error creating children for {current.name}: {str(e)}")
        raise

async def initialize_user_folders(storage: StorageContext) -> None:
    from pyserver.schemas.folder_structure import (
        root_node_id, get_standard_setup, recursively_make_children
    )

    existing_root = await storage.node_storage.get_node(root_node_id())
    if existing_root:
        raise HTTPException(status_code=400, detail="Root folder already exists.")

    setup = get_standard_setup()

    import uuid
    root_node = GraphNode(
        node_id=root_node_id(),  # stable key: 'User'
        object_type="FOLDER",
        caption=setup.name,
        extra_properties={"entry_method": "SYSTEM"}
    )

    await storage.node_storage.store_node(root_node)
    # No parent to index root under, but could optionally add to a "virtual root" here
    await recursively_make_children(storage, setup, root_node)
