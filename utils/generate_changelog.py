"""
This script is used to generate changelog for a repository.
"""

import requests


def get_all_releases(owner, repo):
    """Get all releases of a repository."""

    base_url = f'https://api.github.com/repos/{owner}/{repo}/'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    releases_url = base_url + 'releases'

    release_list = []
    page = 1
    while True:
        params = {'page': page, 'per_page': 100}
        response = requests.get(
            releases_url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            release_list.extend(response.json())
            if 'link' not in response.headers or 'rel="next"' not in response.headers['link']:
                break
            page += 1
        else:
            print(
                f"Failed to fetch releases. Status code: {response.status_code}")

    return release_list


releases = get_all_releases("IamLizu", "wpdetect")

with open("CHANGELOG.md", "w", encoding="utf-8") as changelog_file:
    for release in releases:
        if release['body']:
            changelog_file.write(f"# {release['name']}\n")
            changelog_file.write(f"{release['body']}\n")
