from pathlib import Path
import sys
import click

def get_saved_token():
    token_path = Path.home() / '.urlife' / 'token'
    if token_path.exists():
        return token_path.read_text().strip()
    else:
        click.echo("❌ No JWT token found. Please login first.", err=True)
        sys.exit(1)
