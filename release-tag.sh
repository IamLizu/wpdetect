#!/bin/sh

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
new_version=$($python_executable utils/bump_version.py)


# Tag the release
echo "Tagging version $new_version"
git tag -s "$new_version" -m "release $new_version"

# Generate the changelog
echo "Generating changelog"
git-changelog -o CHANGELOG.md


# Commit the updated version & changelog
echo "Committing version $new_version & changelog"
git add pyproject.toml
git add CHANGELOG.md
git commit -S -m "release $new_version"


# Push the commit and tag
echo "Pushing commit and tag"
# May need to be checked in future if we want to tag a different branch
git push --follow-tags origin master 
