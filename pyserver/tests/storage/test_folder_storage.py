import pytest
import pytest_asyncio
from pyserver.storage.folder_storage import FolderStorage
from pyserver.storage.node_storage import NodeStorage

@pytest.fixture
def test_user_id():
    return "test_user5"

@pytest.fixture
def folder_storage(test_user_id):
    return FolderStorage(test_user_id)

@pytest.fixture
def node_storage(test_user_id):
    return NodeStorage(test_user_id)

@pytest_asyncio.fixture(autouse=True)
async def cleanup_redis(node_storage):
    await node_storage.clear_all_nodes()
    yield
    await node_storage.clear_all_nodes()

@pytest.mark.asyncio
async def test_create_folder_hierarchy(folder_storage, node_storage):
    root_name = "test_root"
    child_name = "test_child"

    # Create root folder
    root_id = await folder_storage.create_folder(root_name)
    assert root_id is not None

    # Lookup root folder
    root_folder = await folder_storage.get_folder_by_name(root_name)
    assert root_folder is not None
    assert root_folder["name"] == root_name
    assert root_folder["object_type"] == "FOLDER"

    # Create child folder
    child_id = await folder_storage.create_folder(child_name, parent_id=root_id)
    assert child_id is not None

    # Lookup child folder
    child_folder = await folder_storage.get_folder_by_name(child_name)
    assert child_folder is not None
    assert child_folder["name"] == child_name
    assert child_folder["object_type"] == "FOLDER"

    # Check parent-child relationship
    child_node = await node_storage.get_node(child_id)
    assert child_node is not None
    assert child_node.parent is not None
    assert child_node.parent.parent_id == root_id
    assert child_node.parent.edge_label == "CHILD_OF"


@pytest.mark.asyncio
async def test_create_duplicate_folder_fails(folder_storage):
    name = "duplicate_test"
    await folder_storage.create_folder(name)
    with pytest.raises(ValueError, match=f"Folder '{name}' already exists"):
        await folder_storage.create_folder(name)


@pytest.mark.asyncio
async def test_get_nonexistent_folder_by_name(folder_storage):
    folder = await folder_storage.get_folder_by_name("nonexistent_folder_123")
    assert folder is None


@pytest.mark.asyncio
async def test_create_nested_folder_tree(folder_storage, node_storage):
    root = await folder_storage.create_folder("root")
    child = await folder_storage.create_folder("child", parent_id=root)
    grandchild = await folder_storage.create_folder("grandchild", parent_id=child)

    grandchild_node = await node_storage.get_node(grandchild)
    assert grandchild_node.parent.parent_id == child


@pytest.mark.asyncio
async def test_get_folder_by_id(folder_storage):
    folder_name = "id_lookup_test"
    folder_id = await folder_storage.create_folder(folder_name)
    folder_info = await folder_storage.get_folder_by_id(folder_id)
    assert folder_info["name"] == folder_name
    assert folder_info["id"] == folder_id


@pytest.mark.asyncio
async def test_list_folder_contents(folder_storage):
    parent_id = await folder_storage.create_folder("parent")
    child1 = await folder_storage.create_folder("child1", parent_id=parent_id)
    child2 = await folder_storage.create_folder("child2", parent_id=parent_id)
    contents = await folder_storage.list_folder_contents(parent_id)
    ids = {child["id"] for child in contents}
    assert ids == {child1, child2}

