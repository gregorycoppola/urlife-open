import click

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """URLife CLI - Interact with URLife services"""
    pass

# Import and register command modules
from urlife import auth
from urlife import folders
from urlife import nodes
from urlife import schemas