import sys

from ao3downloader import strings
from ao3downloader.actions import shared
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository

from tqdm import tqdm

# modified from enterlinks.py

def action(filepath=False):
    """taken from enterlinks.py, gets epubs from list of links file automagically"""
    fileops = FileOps()
    with Repository(fileops) as repo:

        # no prompts! always use epub, always login, never download images
        # filetypes = shared.download_types(fileops)
        # images = shared.images()
        filetypes = ['EPUB']
        images = False
        print(f"You are saving {filetypes[0]}, with downloading images separately set to {str(images).lower()}.")

        if filepath:
            path = filepath
        else:
            print('Enter name of file containing links. (Including file extension)')
            path = input()

        with open(path) as f:
            links = f.readlines()

        # force will login without asking
        shared.ao3_login(repo, fileops, force=True)

        # functional, unchanged
        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, 0, True, images)
        for link in tqdm(links):
            ao3.download(link.strip(), visited)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        action(filepath)
    else:
        action()