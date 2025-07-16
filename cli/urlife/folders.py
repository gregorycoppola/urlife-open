import click
import requests
import sys
import os
from pathlib import Path

from urlife.main import cli

@cli.command("list-folder-direct")
@click.argument('folder-id', required=True)
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
def list_folder(folder_id: str, server: str):
    """List contents of a folder."""
    try:
        click.echo(f"📁 Listing contents of folder: {folder_id}")

        # Load token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ Error: No JWT token found. Please login first.", err=True)
            sys.exit(1)

        token = token_path.read_text().strip()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        url = f"{server}/api/folder/list_direct/{folder_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            nodes = response.json()
            if not nodes:
                click.echo("📭 Folder is empty.")
                return

            click.echo("\n📦 Folder contents:")
            click.echo("-" * 70)
            for node in nodes:
                node_id = node.get("node_id", "???")
                caption = node.get("caption", "")
                node_type = node.get("object_type", "")
                click.echo(f"🆔 {node_id} | 📌 {caption} | 📂 {node_type}")
        elif response.status_code == 404:
            click.echo(f"❌ Folder {folder_id} not found", err=True)
            sys.exit(1)
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Error listing folder contents: {e}", err=True)
        sys.exit(1)

@cli.command("list-folder-recursive")
@click.argument('folder-id', required=True)
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
def list_folder_recursive(folder_id: str, server: str):
    """Recursively list contents of a folder and all its descendants."""
    try:
        click.echo(f"📂 Recursively listing contents of folder: {folder_id}")

        # Load token
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ Error: No JWT token found. Please login first.", err=True)
            sys.exit(1)

        token = token_path.read_text().strip()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        url = f"{server}/api/folder/list_recursive/{folder_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            nodes = response.json()
            if not nodes:
                click.echo("📭 No nodes found under this folder.")
                return

            click.echo("\n📦 Recursive folder contents:")
            click.echo("-" * 70)
            for node in nodes:
                node_id = node.get("node_id", "???")
                caption = node.get("caption", "")
                node_type = node.get("object_type", "")
                click.echo(f"🆔 {node_id} | 📌 {caption} | 📂 {node_type}")
        elif response.status_code == 404:
            click.echo(f"❌ Folder {folder_id} not found", err=True)
            sys.exit(1)
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Error listing recursive folder contents: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
def get_root_folder_id(server: str):
    """Get the ID of the root folder."""
    try:
        click.echo("Getting root folder ID...")

        token_path = Path.home() / '.urlife' / 'token'
        if token_path.exists():
            with open(token_path, 'r') as f:
                token = f.read().strip()
        else:
            click.echo("❌ Error: No JWT token found. Please login first.", err=True)
            sys.exit(1)

        headers = {
            'Authorization': f'Bearer {token}'
        }
        url = f"{server}/api/folder/root_id"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        folder_id = response.text
        click.echo(f"Root folder ID: {folder_id}")

    except requests.exceptions.RequestException as e:
        click.echo(f"❌ Error getting root folder ID: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('node-id', required=True)
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
@click.option('--verbose', is_flag=True, help='Show full node data instead of just caption/type')
def path_to_root(node_id: str, server: str, verbose: bool):
    """Get the path from a node up to the root."""
    try:
        click.echo(f"🔎 Getting path to root for node: {node_id}")

        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ Error: No JWT token found. Please login first.", err=True)
            sys.exit(1)

        token = token_path.read_text().strip()
        headers = {'Authorization': f'Bearer {token}'}
        url = f"{server}/api/folder/path_to_root/{node_id}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            path = response.json()
            if not path:
                click.echo("⚠️  No path found (is this an orphan node?)")
                return

            click.echo("\n🧭 Path to root:")
            click.echo("-" * 50)
            for step in path:
                edge_label = step.get('edge_label', 'UNKNOWN')
                node = step.get('node', {})
                if verbose:
                    click.echo(f"edge_label: {edge_label}\nnode: {node}\n---")
                else:
                    caption = node.get("caption", "<no caption>")
                    object_type = node.get("object_type", "UNKNOWN")
                    node_id = node.get("node_id", "???")
                    click.echo(f"{edge_label} → {caption} [{object_type}] ({node_id})")
            click.echo("-" * 50)
        elif response.status_code == 404:
            click.echo(f"❌ Node {node_id} not found", err=True)
            sys.exit(1)
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)

@cli.command("create-folder")
@click.argument('parent_id', required=True)
@click.argument('name', required=True)
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
def create_folder(parent_id: str, name: str, server: str):
    """Create a new folder for the current user.

    PARENT_ID: The parent folder ID (required)
    NAME: The name of the new folder (required)
    """
    try:
        token_path = Path.home() / '.urlife' / 'token'
        if not token_path.exists():
            click.echo("❌ Error: No JWT token found. Please login first.", err=True)
            sys.exit(1)
        token = token_path.read_text().strip()

        data = {"name": name, "parent_id": parent_id}

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        url = f"{server}/api/folder/create"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            click.echo(f"✅ Folder created. ID: {result.get('id', '[unknown]')}")
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)
    except requests.RequestException as e:
        click.echo(f"❌ Network error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)

# append here