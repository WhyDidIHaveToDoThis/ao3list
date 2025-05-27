import AO3
from time import time

url = input("What is the url for the story you want comments for?\n")
# test url
# url = "https://archiveofourown.org/works/43334320"
# get metadata, add to title of markdown file
workid = AO3.utils.workid_from_url(url)
work = AO3.Work(workid)
authorslist = []
for author in work.authors:
		authorslist.append(f"{author.username}")
authors = ', '.join(authorslist)
output = open(f"{work.title} by {authors} - comments.md", 'a')

# get the number of comments (idk if this gets it for all chapters)
numcomment = work.comments
work.load_chapters()

# start a timer
start = time()

# load every comment threat found
comments = work.get_comments(numcomment)

# loading message
print(f"Loaded {len(comments)} comment threads in {round(time()-start, 1)} seconds\n")

# loop through all comments
for comment in comments:
	output.write(f"Comment ID: {comment.id}\n")
	output.write(f"Author: [{comment.author.username}]({comment.author.url})\n")
	output.write(f"Replies: {len(comment.get_thread())}\n")
	output.write(f"- {comment.text}\n")
	
	#get thread
	for comment in comment.get_thread():
		output.write(f"Comment ID: {comment.id}\n")
		output.write(f"Author: [{comment.author.username}]({comment.author.url})\n")
		output.write(f"- {comment.text}\n")

	# separate with line
	output.write("---\n")
output.close()

# print finished
print(f"Finished getting comments in {round(time()-start, 1)} seconds!")

