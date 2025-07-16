import pytest
from fastapi import HTTPException
from pyserver.schemas.folder_structure import initialize_user_folders, FolderNames
from pyserver.storage.storage_context import StorageContext
from pyserver.system.graph_node import GraphNode

TEST_USER_ID = "test_user_folder_init"

@pytest.mark.asyncio
async def test_initialize_user_folders_creates_expected_structure():
    storage = StorageContext(TEST_USER_ID)
    await storage.node_storage.clear_all_nodes()
    await storage.folder_tracker.clear_all_indexes()

    await initialize_user_folders(storage)

    all_nodes = await storage.node_storage.get_all_nodes()
    all_captions = {node.caption for node in all_nodes}

    expected = {
        FolderNames.USER,
        FolderNames.INBOX,
        FolderNames.JOURNAL,
        FolderNames.PROJECTS,
        FolderNames.BUSINESS,
        FolderNames.PRODUCT,
        FolderNames.HOME,
        FolderNames.MONEY,
        FolderNames.LIFE,
        FolderNames.BODY,
        FolderNames.SOCIAL,
        FolderNames.PEOPLE,
    }

    assert expected.issubset(all_captions), "All standard folders should be created"

@pytest.mark.asyncio
async def test_project_children_indexed_correctly():
    storage = StorageContext(TEST_USER_ID)
    await storage.node_storage.clear_all_nodes()
    await storage.folder_tracker.clear_all_indexes()

    await initialize_user_folders(storage)

    all_nodes = await storage.node_storage.get_all_nodes()
    projects_node = next(node for node in all_nodes if node.caption == FolderNames.PROJECTS)

    children_ids = await storage.folder_tracker.list_direct(projects_node.node_id)
    children = [await storage.node_storage.get_node(child_id) for child_id in children_ids]
    child_names = sorted(child.caption for child in children)

    expected = sorted([
        FolderNames.BUSINESS,
        FolderNames.PRODUCT,
        FolderNames.HOME,
        FolderNames.MONEY,
        FolderNames.LIFE,
        FolderNames.BODY,
        FolderNames.SOCIAL,
    ])
    assert child_names == expected, "Projects folder should contain expected subfolders"

@pytest.mark.asyncio
async def test_initialize_twice_raises_http_exception():
    storage = StorageContext(TEST_USER_ID)
    await storage.node_storage.clear_all_nodes()
    await storage.folder_tracker.clear_all_indexes()

    await initialize_user_folders(storage)

    with pytest.raises(HTTPException) as exc_info:
        await initialize_user_folders(storage)

    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail
