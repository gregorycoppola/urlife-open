from typing import Optional, Dict, Any
import secrets
import time
from pyserver.system.graph_node import GraphNode, ParentRef, ChildRef
from pyserver.storage.storage_context import StorageContext
from fastapi import HTTPException
from pyserver.schemas.type_properties import ExtraProperties, get_extra_properties_for_type

def generate_default_properties(props: ExtraProperties) -> dict:
    result = {}

    for checkbox in props.checkbox_questions:
        result[checkbox.key_name] = False

    for radio in props.radio_questions:
        result[radio.key_name] = radio.options[0].value if radio.options else None

    for number in props.number_questions:
        result[number.key_name] = number.default

    for date in props.date_questions:
        result[date.key_name] = {
            "date": None if date.has_date else None,
            "time": None if date.has_time else None,
        }

    return result

async def create_node_under_folder(
    storage: StorageContext,
    folder_id: str,
    object_type: str,
    caption: str,
) -> GraphNode:
    """
    Core logic to create a node inside a folder.
    Automatically populates extra_properties based on the type.
    """
    # Step 1: Validate folder exists
    folder = await storage.folder_storage.get_folder_by_id(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail=f"Folder {folder_id} not found")

    # Step 2: Get default properties for the type
    type_properties = get_extra_properties_for_type(object_type)
    default_props = generate_default_properties(type_properties)

    # Step 3: Create new node
    node_id = secrets.token_hex(16)
    now = int(time.time())
    node = GraphNode(
        node_id=node_id,
        object_type=object_type,
        caption=caption,
        extra_properties=default_props,
        creation_time=now,
        parent=ParentRef(edge_label="CHILD_OF", parent_id=folder_id),
    )
    await storage.node_storage.store_node(node)

    # Step 4: Update parent folder's children
    folder_node = await storage.node_storage.get_node(folder_id)
    children = folder_node.children or {}
    edge_label = "CHILDREN"
    children.setdefault(edge_label, []).append(
        ChildRef(edge_label=edge_label, child_id=node_id)
    )
    folder_node.children = children
    await storage.node_storage.store_node(folder_node)

    # Step 5: Index in folder tracker
    await storage.folder_tracker.add_to_folder(folder_id, node_id)

    return node
