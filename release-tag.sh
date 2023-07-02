#!/bin/sh

echo "Running release-tag.sh"

# Run the version bumping script
new_version=$(python utils/bump_version.py)

# Commit the updated version
echo "Committing version $new_version"
git add pyproject.toml
git commit -S -m "release $new_version"

# Tag the release
echo "Tagging version $new_version"
git tag -s "$new_version" -m "release $new_version"

# Push the commit and tag
echo "Pushing commit and tag"
git push --follow-tags origin master
