"""
    This file increments the version in pyproject.toml.
"""

import os
import toml


def write_changes_to_file(file_location, checker, version):
    """Writes the changes to the file."""

    with open(file_location, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    with open(file_location, 'w', encoding="utf-8") as file:
        for line in lines:
            if line.startswith(checker):
                file.write(f'{checker} = "{version}"\n')
            else:
                file.write(line)


def increment_version():
    """Increments the version in pyproject.toml and returns the new version."""

    file_path = os.path.join(os.path.dirname(
        __file__), '..', 'pyproject.toml')

    with open(file_path, 'r', encoding="utf-8") as file:
        config = toml.load(file)

    current_version = config['project']['version']

    # Increment the version
    version_parts = current_version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)

    # Update the version in pyproject.toml
    write_changes_to_file(file_path, 'version', new_version)

    # Update the version in wpdetect/constants.py
    write_changes_to_file('wpdetect/constants.py', 'VERSION', new_version)

    return new_version


# Call the increment_version() function
BUMPED_VERSION = increment_version()
print(f"v{BUMPED_VERSION}")
