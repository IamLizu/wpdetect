#!/bin/sh

# Run the version bumping script
new_version=$(python wpdetect\utils\bump_version.py)

# Commit the updated version
git add pyproject.toml
git commit -S -m "release v$new_version"

# Tag the release
git tag -s "v$new_version" -m "release v$new_version"
