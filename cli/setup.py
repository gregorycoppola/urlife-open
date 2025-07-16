from setuptools import setup, find_packages

setup(
    name="urlife",
    version="0.1.0",
    description="URLife CLI - Command line interface for interacting with URLife services",
    author="coppola.ai",
    packages=find_packages(),  # Finds 'commands'
    install_requires=[
        "click>=8.0",     # CLI framework
        "requests>=2.25"  # For HTTP API calls
    ],
    entry_points={
        "console_scripts": [
            "urlife = urlife.main:cli"
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
