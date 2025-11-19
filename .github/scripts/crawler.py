
...
import requests
import json
from bs4 import BeautifulSoup
import os, sys

def get_favicon(site_url):
    found_favicon = ""
    response = requests.get(site_url, timeout=3)
    if response.status_code != 200:
        return found_favicon
    found_favicon = f"{site_url.rstrip('/')}/favicon.ico"
    soup = BeautifulSoup(response.text, "html.parser")
    icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
    if icon_link and icon_link.get("href"):
        print(icon_link["href"])
        found_favicon = requests.compat.urljoin(site_url, icon_link["href"])
    return found_favicon

def get_github_pages_sites(base_url, username, token):
    visited = set()
    sites = []
    page = 1
    print(f'Base: {base_url}, name: {username}')
    while True:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(repos_url, headers={"Authorization": f"token {token}"})
        if response.status_code != 200:
            raise Exception(f"Error fetching repos: {response.status_code}")
        repos = response.json()
        if not repos:
            break
        print(f"Found {len(repos)} repositories on page {page}.")
        for repo in repos:
            pages_url = f"https://api.github.com/repos/{username}/{repo['name']}/pages"
            pages_response = requests.get(pages_url, headers={"Authorization": f"token {token}"})
            print(str(pages_response))
            if pages_response.status_code == 200:
                site_url = f"{base_url}{repo["name"]}"
                favicon = get_favicon(site_url)
                found_repo = {
                    "sitename" : f"/{repo['name']}",
                    "favicon" : favicon
                }
                #sites.append(site_url)
                sites.append(found_repo)
        page += 1
    return sites

def save_sites_to_json(base_url, username, token, filename="endpoints.json"):
    sites = get_github_pages_sites(base_url, username, token)
    data = {"base url": base_url, "sites": sites}
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(sites)} sites to {filename}.")

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("Please set your GitHub token in the GITHUB_TOKEN environment variable.")
    given_base_url = sys.argv[1]  # pass in a URL 
    given_username = sys.argv[2] # pass in the username separately
    save_sites_to_json(given_base_url, given_username, token)
