"""
This module contains a function to increment the version in pyproject.toml.
"""

import os
import toml


def increment_version():
    """Increments the version in pyproject.toml and returns the new version."""

    file_path = os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml')

    with open(file_path, 'r', encoding="utf-8") as file:
        config = toml.load(file)

    current_version = config['project']['version']

    # Increment the version
    version_parts = current_version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)

    # Update the version in pyproject.toml
    config['project']['version'] = new_version

    # Write the updated version back to pyproject.toml
    file_path = os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml')

    with open(file_path, 'r', encoding="utf-8") as file:
        toml.dump(config, file)

    return new_version


# Call the increment_version() function
BUMPED_VERSION = increment_version()
print(f"Version bumped to: {BUMPED_VERSION}")
