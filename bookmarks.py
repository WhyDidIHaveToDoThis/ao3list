import AO3
from time import time

session = AO3.Session("username", "password")

filename = input("Name of file with links, include .txt\n")

with open('filename', 'r') as file:
    # Read each line in the file
    for line in file:
        url = line.strip()
		workid = AO3.utils.workid_from_url(url)
		work = AO3.Work(workid, session=sess)
		work.bookmark()
		# figure out how to deal with errors and log errors
		
print(f"Finished bookmarking links in {round(time()-start, 1)} seconds!")

