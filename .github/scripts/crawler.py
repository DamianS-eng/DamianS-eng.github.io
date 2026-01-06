import requests
import json
from bs4 import BeautifulSoup
import favicon
import os, sys

def get_favicon(site_url):
    default_icon_path = site_url.rstrip("/" + "/favicon.ico")
    try:
        icons = favicon.get(site_url)
        if icons:
            print(f"{site_url} has these icons:")
            for icon in icons:
                print(icon.url)
            return icons[0].url
        else:
            return default_icon_path
    except Exception as e:
        print(f"Problem getting favicon for {site_url}: {e}")
    return default_icon_path

def get_favicon_and_title(site_url):
    site_title = ""
    found_favicon = get_favicon(site_url)
    response = requests.get(site_url, timeout=3)
    if response.status_code != 200:
        return (found_favicon, site_title)
    # found_favicon = f"{site_url.rstrip('/')}/favicon.ico"
    soup = BeautifulSoup(response.text, "html.parser")
    site_title = soup.title.string if soup.title else ""
    # icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
    # if icon_link and icon_link.get("href"):
        # found_favicon = requests.compat.urljoin(site_url, icon_link["href"])
        # print(f"Expected found icon: {site_title}, : {icon_link['href']} : {found_favicon}")
    return (found_favicon, site_title)

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
                favicon, title = get_favicon_and_title(site_url)
                found_repo = {
                    "sitename" : f"/{repo['name']}",
                    "favicon" : favicon,
                    "title" : title
                }
                sites.append(found_repo)
        page += 1
    return sites

def save_sites_to_json(base_url, username, token, filename="endpoints.json"):
    sites = get_github_pages_sites(base_url, username, token)
    data = {"base url": base_url, "sites": sites}
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(sites)} sites to {filename}.")
    with open("temp_number_added_sites.txt", "w") as f:
        f.write("{len(sites)}")

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("Please set your GitHub token in the GITHUB_TOKEN environment variable.")
    given_base_url = sys.argv[1]  # pass in a URL 
    given_username = sys.argv[2] # pass in the username separately
    save_sites_to_json(given_base_url, given_username, token)
