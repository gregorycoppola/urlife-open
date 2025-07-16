import pytest
from pyserver.schemas.folder_structure import initialize_user_folders, FolderNames
from pyserver.storage.storage_context import StorageContext

TEST_USER_ID = "test_user_nuke"

@pytest.mark.asyncio
async def test_nuke_all_data_removes_nodes_and_indices():
    # Create a storage context and initialize folder structure
    storage = StorageContext(TEST_USER_ID)
    await storage.node_storage.clear_all_nodes()
    await storage.folder_tracker.clear_all_indexes()
    
    await initialize_user_folders(storage)

    # Sanity check: data exists
    all_nodes = await storage.node_storage.get_all_nodes()
    assert len(all_nodes) > 0, "Expected nodes to exist after initialization"

    some_folder = next((n for n in all_nodes if n.caption == FolderNames.PROJECTS), None)
    assert some_folder, "Expected to find Projects folder"

    folder_index = await storage.folder_tracker.list_direct(some_folder.node_id)
    assert len(folder_index) > 0, "Expected folder to have children in direct index"

    # Run the same logic as nuke_all_data route
    await storage.node_storage.clear_all_nodes()
    await storage.folder_tracker.clear_all_indexes()

    # Now check everything is gone
    remaining_nodes = await storage.node_storage.get_all_nodes()
    assert remaining_nodes == [], "Expected all nodes to be deleted"

    index_after = await storage.folder_tracker.list_direct(some_folder.node_id)
    assert index_after == set() or index_after == [], "Expected folder index to be empty"
