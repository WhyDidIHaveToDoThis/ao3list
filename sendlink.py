import sys
import os
import json

from ao3downloader import strings
from ao3downloader.actions import shared
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository

from tqdm import tqdm

# modified from ao3download.py and enterlinks.py

def downloadfromlink(rawlink, numpages=1):
    """Takes ao3 link and downloads all works from specified pages"""
    fileops = FileOps()
    with Repository(fileops) as repo:

        # Always EPUB, series, no images, default to one page
        filetypes = ['EPUB']
        series = True
        images = False

        link = rawlink.strip()
        pages = int(numpages)

        testiflink(link)

        # account = loadaccount()
        # print('logging in')
        # repo.login(account['username'], account['password'])
        # print('login success')

        shared.ao3_login(repo, fileops, force=True)

        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, pages, series, images)
        ao3.download(link, visited)

def linkfromfile(filepath=False, numpages=1):
    """Takes long link from file and downloads all works from specified pages"""
    fileops = FileOps()
    with Repository(fileops) as repo:

        # Always EPUB, series, no images, default to one page
        filetypes = ['EPUB']
        series = True
        images = False
        
        path = filepath
        pages = int(numpages)

        with open(path) as f:
            links = f.readlines()

        print(links)
        link = links[0].strip()
        testiflink(link)
        print(link)

        shared.ao3_login(repo, fileops, force=True)

        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, pages, series, images)

        ao3.download(link, visited)


def testiflink(testlink):
    """Check if AO3 link and integer before passing"""
    if testlink.startswith("https://archiveofourown.org"):
        return
    else:
        print('Either pass raw AO3 link or text file containing link and number of pages to download.')
        exit()

def loadaccount():
    """Load account from details saved in the JSON file."""
    settings_file = 'settings.json'

    if not os.path.exists(settings_file):
        print(f"Error: {settings_file} not found!")
        exit(1)

    with open(settings_file, 'r') as f:
        settings = json.load(f)

    # Extract username and password from the settings file
    username = settings.get('username')
    password = settings.get('password')

    return {'username': username, 'password': password}

if __name__ == "__main__":
    if len(sys.argv) == 3:
        rawinput = sys.argv[1].strip("\"")
        print(rawinput)
        numpages = sys.argv[2]
        if rawinput.endswith('.txt'):
            linkfromfile(rawinput, numpages)
        else:
            downloadfromlink(rawinput, numpages)
    elif len(sys.argv) == 2:
        rawinput = sys.argv[1]
        print(rawinput)
        if rawinput.endswith('.txt'):
            linkfromfile(rawinput)
        else:
            downloadfromlink(rawinput)
    else:
        print('Either pass raw AO3 link or text file containing link and number of pages to download.')
        exit()