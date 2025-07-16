import click
import requests
import sys
from pathlib import Path
from urlife.main import cli  # wherever your main cli group is defined
from datetime import datetime

@cli.command("create-node-in-folder")
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
@click.option('--folder-id', '-f', required=True, help='Folder ID to create the node in')
@click.option('--type', '-T', required=True, help='Type of the node')
@click.option('--caption', '-c', required=True, help='Caption for the node')
def create_node(server: str, folder_id: str, type: str, caption: str):
    """
    Create a new node.

    Example:
        urlife create-node-in-folder -T GOAL -c "My Goal" -f User
    """
    try:
        # Load token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        data = {
            "folder_id": folder_id,
            "object_type": type,
            "caption": caption
        }

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(f"{server}/api/node/create/in_folder", headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            click.echo(f"✅ Node created: {result['node_id']}")
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Error creating node: {e}", err=True)
        sys.exit(1)

@cli.command("create-node-as-child")
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
@click.option('--parent-id', '-p', required=True, help='Parent node ID')
@click.option('--label', '-l', required=True, help='Child label (edge label)')
@click.option('--type', '-T', required=True, help='Type of the node')
@click.option('--caption', '-c', required=True, help='Caption for the node')
def create_node_as_child(server: str, parent_id: str, label: str, type: str, caption: str):
    """
    Create a new node as a labeled child under a non-folder parent.

    Example:
        urlife create-node-as-child -T GOAL -c "Step 1" -p abc123 -l subgoal
    """
    try:
        # Load JWT token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        data = {
            "parent_id": parent_id,
            "edge_label": label,
            "object_type": type,
            "caption": caption
        }

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(f"{server}/api/node/create/as_child", headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            click.echo(f"✅ Node created as child: {result['node_id']}")
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Error creating child node: {e}", err=True)
        sys.exit(1)

def print_node_pretty(node: dict):
    click.echo("✅ Node Details")
    click.echo("───────────────")
    click.echo(f"ID:            {node.get('node_id')}")
    click.echo(f"Type:          {node.get('object_type')}")
    click.echo(f"Caption:       {node.get('caption')}")

    ep = node.get("extra_properties", {})
    click.echo(f"Status:        {ep.get('status', '-')}")
    click.echo(f"Priority:      {ep.get('priority', '-')}")
    click.echo(f"Attention:     {ep.get('attention', '-')}")

    click.echo("Flags:")
    for flag in ["Urgent", "Critical", "Needs Decision", "Active"]:
        click.echo(f"  - {flag:15}: {ep.get(flag, False)}")

    parent = node.get("parent")
    if parent:
        click.echo(f"Parent:        {parent.get('parent_id')} (edge: {parent.get('edge_label')})")

    ts = node.get("creation_time")
    if ts:
        dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
        click.echo(f"Created At:    {dt}")


@cli.command("read-node")
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
@click.argument('node_id')
def read_node(server: str, node_id: str):
    """
    Read a node by ID and print the result.

    Example:
        urlife read-node <NODE_ID>
    """
    try:
        # Load token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(f"{server}/api/node/read/node/{node_id}", headers=headers)
        if response.status_code == 200:
            node = response.json()
            print_node_pretty(node)
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)
    except requests.RequestException as e:
        click.echo(f"❌ Error reading node: {e}", err=True)
        sys.exit(1)

@cli.command("update-node-caption")
@click.argument("node_id")
@click.argument("caption")
@click.option("--server", "-s", default="http://localhost:8000", help="URLife API server URL")
def update_node_caption(node_id: str, caption: str, server: str):
    """
    Update the caption of a node.

    Example:
        urlife update-node-caption abc123 "New Caption"
    """
    try:
        # 🔐 Load token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "node_id": node_id,
            "new_caption": caption
        }

        response = requests.post(f"{server}/api/node/update/caption", headers=headers, json=payload)

        if response.status_code == 200:
            click.echo(f"✅ Caption updated for node {node_id}")
        else:
            click.echo(f"❌ Error {response.status_code}: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)

@cli.command("update-node-checkbox")
@click.argument("node_id")
@click.argument("key_name")
@click.argument("value", type=bool)
@click.option("--server", "-s", default="http://localhost:8000", help="URLife API server URL")
def update_checkbox(node_id: str, key_name: str, value: bool, server: str):
    """
    Update a checkbox field on a node.

    Example:
        urlife update-checkbox abc123 "Urgent" true
    """
    try:
        # 🔐 Load token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "node_id": node_id,
            "key_name": key_name,
            "value": value
        }

        response = requests.post(f"{server}/api/node/update/checkbox", headers=headers, json=payload)

        if response.status_code == 200:
            click.echo(f"✅ Checkbox '{key_name}' updated to {value} for node {node_id}")
        else:
            click.echo(f"❌ Error {response.status_code}: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)

@cli.command("update-node-radio")
@click.argument("node_id")
@click.argument("key_name")
@click.argument("value")  # radio values are strings
@click.option("--server", "-s", default="http://localhost:8000", help="URLife API server URL")
def update_node_radio(node_id: str, key_name: str, value: str, server: str):
    """
    Update a radio field on a node.

    Example:
        urlife update-node-radio abc123 "status" "closed"
    """
    try:
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "node_id": node_id,
            "field": key_name,
            "value": value
        }

        response = requests.post(f"{server}/api/node/update/radio", headers=headers, json=payload)

        if response.status_code == 200:
            click.echo(f"✅ Radio field '{key_name}' updated to '{value}' for node {node_id}")
        else:
            click.echo(f"❌ Error {response.status_code}: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)

@cli.command("update-node-number")
@click.argument("node_id")
@click.argument("key_name")
@click.argument("value", type=int)
@click.option("--server", "-s", default="http://localhost:8000", help="URLife API server URL")
def update_node_number(node_id: str, key_name: str, value: int, server: str):
    """
    Update a numeric field on a node.

    Example:
        urlife update-node-number abc123 "attention" 42
    """
    try:
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "node_id": node_id,
            "field": key_name,
            "value": value
        }

        response = requests.post(f"{server}/api/node/update/number", headers=headers, json=payload)

        if response.status_code == 200:
            click.echo(f"✅ Number field '{key_name}' updated to {value} for node {node_id}")
        else:
            click.echo(f"❌ Error {response.status_code}: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)


# append here

@cli.command("read-node-children")
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
@click.argument('node_id')
@click.option('--edge-label', '-l', required=True, help='Edge label to filter children by')
def read_node_children(server: str, node_id: str, edge_label: str):
    """
    Get children of a node filtered by edge label.

    Example:
        urlife read-node-children <NODE_ID> --edge-label subgoal
    """
    try:
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        url = f"{server}/api/node/read/children/{node_id}"
        params = {'edge_label': edge_label}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            children = response.json()
            if not children:
                click.echo(f"No children found for node {node_id} with edge label '{edge_label}'.")
            else:
                click.echo(f"Children of node {node_id} (edge label: '{edge_label}'):")
                for child in children:
                    click.echo(f"- {child['node_id']} | {child['caption']} | {child['object_type']} | Created: {child.get('creation_time', 'N/A')}")
        else:
            click.echo(f"❌ Error {response.status_code}: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)

@cli.command("search-nodes")
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
@click.option('--root-id', '-r', required=True, help='Root folder ID to start the search')
@click.option('--object-type', '-t', required=True, help='Object type to filter (e.g., GOAL, VISION)')
@click.option('--query', '-q', required=True, help='Search query string to fuzzy match against node captions')
@click.option('--limit', '-l', default=20, help='Maximum number of results to return')
def search_nodes(server: str, root_id: str, object_type: str, query: str, limit: int):
    """
    Search nodes under a root folder by object type and fuzzy match.

    Example:
        urlife search-nodes --root-id <FOLDER_ID> --object-type GOAL --query "health" --limit 10
    """
    try:
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        url = f"{server}/api/node/search"
        payload = {
            'root_id': root_id,
            'object_type': object_type,
            'query': query,
            'limit': limit
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            results = response.json()
            if not results:
                click.echo("No matching nodes found.")
            else:
                click.echo(f"Top {len(results)} matches:")
                for node in results:
                    click.echo(
                        f"- [{node['match_score']}] {node['node_id']} | {node['caption']} | {node['object_type']} | Created: {node.get('creation_time', 'N/A')}"
                    )
        else:
            click.echo(f"❌ Error {response.status_code}: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)
