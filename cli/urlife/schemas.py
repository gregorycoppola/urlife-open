import click
import requests
from pathlib import Path
import sys
from urlife.main import cli
from urlife.utils import get_saved_token
import json

@cli.command("all-type-properties")
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
def all_type_properties(server: str):
    """Get type properties for nodes.

    Args:
      --server: URL of the URLife API server (default: http://localhost:8000)

    Examples:
      urlife all-type-properties
    """
    try:
        # Get type properties
        response = requests.get(f"{server}/api/schema/all-type-properties")
        response.raise_for_status()
        
        # Pretty print the response without truncation
        properties = response.json()
        click.echo("Type Properties:")
        click.echo("-" * 50)
        click.echo(json.dumps(properties, indent=2))
        click.echo("-" * 50)
        
    except requests.RequestException as e:
        click.echo(f"Error fetching type properties: {e}", err=True)
        sys.exit(1)

