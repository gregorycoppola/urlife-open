import click
import requests
from pathlib import Path
import sys
from urlife.main import cli
from urlife.utils import get_saved_token

@cli.command()
@click.option('--email', '-e', required=True, help='User email')
@click.option('--password', '-p', required=True, help='User password')
@click.option('--server', '-s', default='http://localhost:8000', help='URLife API server URL')
def login(email: str, password: str, server: str):
    """
    Login to URLife and get a JWT token.
    """
    try:
        login_data = {
            'username': email,
            'password': password
        }

        response = requests.post(f"{server}/api/auth/login", data=login_data)
        response.raise_for_status()

        data = response.json()
        token = data['access_token']
        click.echo("✅ Login successful!")
        click.echo(f"Access Token: {token}")

        # 🔐 Always save token
        token_dir = Path.home() / '.urlife'
        token_dir.mkdir(parents=True, exist_ok=True)
        token_file = token_dir / 'token'
        token_file.write_text(token)
        click.echo(f"🔐 Token saved to {token_file}")

    except requests.RequestException as e:
        click.echo(f"❌ Error logging in: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--server', '-s', default='http://localhost:8000', help='URL of the URLife API server')
def whoami(server: str):
    """
    Get information about the currently authenticated user.
    """
    from urlife.utils import get_saved_token

    try:
        token = get_saved_token()

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(f"{server}/api/auth/me", headers=headers)

        if response.status_code == 200:
            user = response.json()
            click.echo(f"👤 User ID: {user['user_id']}")
            click.echo(f"📧 Email: {user['email']}")
            click.echo(f"📛 Name: {user.get('name', 'N/A')}")
            click.echo(f"✅ Active: {user['is_active']}")
        else:
            click.echo(f"❌ Error: {response.status_code} - {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Error fetching user info: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--email', '-e', required=True, help='User email')
@click.option('--password', '-p', required=True, help='User password')
@click.option('--name', '-n', required=True, help='Full name of the user')
@click.option('--server', '-s', default='http://localhost:8000', help='URL of the URLife API server')
def register(email: str, password: str, name: str, server: str):
    """
    Register a new user account.
    """
    try:
        registration_data = {
            'email': email,
            'password': password,
            'name': name
        }

        click.echo("\n🔍 Registering new user...")
        click.echo(f"📌 Server: {server}")
        click.echo(f"📌 Email: {email}")
        click.echo(f"📌 Name: {name}")

        response = requests.post(
            f"{server}/api/auth/register",
            json=registration_data
        )

        if response.status_code == 200:
            data = response.json()
            click.echo("\n✅ Registration successful!")
            click.echo(f"User ID: {data['user_id']}")
        else:
            click.echo(f"\n❌ Registration failed: {response.status_code}", err=True)
            try:
                click.echo(f"Error: {response.json().get('detail')}", err=True)
            except Exception:
                click.echo(f"Error: {response.text}", err=True)
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(f"❌ Error registering: {e}", err=True)
        sys.exit(1)
