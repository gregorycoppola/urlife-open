import pytest
from pyserver.storage.node_factory import create_node_under_folder
from pyserver.storage.storage_context import StorageContext
from pyserver.system.graph_node import GraphNode
from pyserver.schemas.type_properties import get_extra_properties_for_type

@pytest.fixture
def storage_context():
    # Use a unique user id for isolation
    return StorageContext("test_user_fixture")

@pytest.fixture
def create_test_folder(storage_context):
    async def _create(name):
        return await storage_context.folder_storage.create_folder(name)
    return _create

@pytest.mark.asyncio
async def test_create_goal_node_sets_expected_defaults(storage_context: StorageContext, create_test_folder):
    folder_id = await create_test_folder("test_goal_defaults")
    node = await create_node_under_folder(storage_context, folder_id, "GOAL", "Goal Node")

    defaults = node.extra_properties
    expected_keys = {q.key_name for q in get_extra_properties_for_type("GOAL").radio_questions}
    expected_keys.update(q.key_name for q in get_extra_properties_for_type("GOAL").checkbox_questions)
    expected_keys.update(q.key_name for q in get_extra_properties_for_type("GOAL").number_questions)

    # Assert all expected fields are present
    assert set(defaults.keys()) == expected_keys

    # Spot-check values
    assert defaults["status"] == "open"  # First radio option
    assert defaults["attention"] == 0  # From priority question
    assert defaults["Active"] is False  # One of the checkbox keys

@pytest.mark.asyncio
async def test_create_event_node_sets_expected_defaults(storage_context: StorageContext, create_test_folder):
    folder_id = await create_test_folder("test_event_defaults")
    node = await create_node_under_folder(storage_context, folder_id, "EVENT", "Event Node")

    defaults = node.extra_properties
    assert defaults["evaluation"] == "positive"
    assert defaults["event_size"] == "small"
    assert defaults["attention"] == 0

@pytest.mark.asyncio
async def test_create_thought_node_has_no_extra_properties(storage_context: StorageContext, create_test_folder):
    folder_id = await create_test_folder("test_thought_defaults")
    node = await create_node_under_folder(storage_context, folder_id, "THOUGHT", "Thought Node")

    assert node.extra_properties == {}
