#!/bin/sh

# This script is used to tag a release of the package.

echo "Running release-tag.sh"

# Ensure we're on the master branch
if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then
    echo "Not on master branch, aborting"
    exit 1
fi

# Find the python executable
python_executable=$(which python)
if [ -z "$python_executable" ]; then
    python_executable=$(which python3)
fi


# Run the version bumping script
new_version=$($python_executable bump_version.py)

# Commit the updated version
echo "Committing version $new_version"
git add pyproject.toml
git add wpdetect/__main__.py
git commit -S -m "release $new_version"


# Tag the release
echo "Tagging version $new_version"
git tag -s "$new_version" -m "release $new_version"

# Generate the changelog
echo "Generating changelog"
git-changelog -o CHANGELOG.md

# Commit (ammend) the changelog
echo "Committing changelog"
git add CHANGELOG.md
git commit --amend --no-edit

# Tag the release again (with the changelog)
git tag -d "$new_version"
git tag -s "$new_version" -m "release $new_version"

# Push the commit and tag
echo "Pushing commit and tag"
# May need to be checked in future if we want to tag a different branch
git push --follow-tags origin master 
