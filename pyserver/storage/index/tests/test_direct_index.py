import pytest
import uuid
from pyserver.storage.index.direct import DirectFolderIndex

TEST_USER_ID = "test_user_direct_index"

@pytest.mark.asyncio
async def test_add_and_list():
    index = DirectFolderIndex(TEST_USER_ID)
    await index.clear_all_direct_indexes()

    folder_id = "folder_" + str(uuid.uuid4())
    node_ids = [f"node_{uuid.uuid4()}" for _ in range(3)]

    # Add nodes
    for node_id in node_ids:
        await index.add(folder_id, node_id)

    result = await index.list(folder_id)

    assert set(result) == set(node_ids), "List contents should match added nodes"

@pytest.mark.asyncio
async def test_remove():
    index = DirectFolderIndex(TEST_USER_ID)
    await index.clear_all_direct_indexes()

    folder_id = "folder_" + str(uuid.uuid4())
    node_id = f"node_{uuid.uuid4()}"

    await index.add(folder_id, node_id)
    contents_before = await index.list(folder_id)
    assert node_id in contents_before

    await index.remove(folder_id, node_id)
    contents_after = await index.list(folder_id)
    assert node_id not in contents_after

@pytest.mark.asyncio
async def test_clear_all_direct_indexes():
    index = DirectFolderIndex(TEST_USER_ID)
    await index.clear_all_direct_indexes()

    folder_1 = f"folder_{uuid.uuid4()}"
    folder_2 = f"folder_{uuid.uuid4()}"

    await index.add(folder_1, "node_a")
    await index.add(folder_2, "node_b")

    # Confirm data exists
    assert set(await index.list(folder_1)) == {"node_a"}
    assert set(await index.list(folder_2)) == {"node_b"}

    # Clear all
    await index.clear_all_direct_indexes()

    assert set(await index.list(folder_1)) == set()
    assert set(await index.list(folder_2)) == set()

