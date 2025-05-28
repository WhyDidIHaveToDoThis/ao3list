# Random scripts that I use to manage AO3 epub downloads

## using [ao3_api](https://github.com/wendytg/ao3_api)
### comments.py
- uses ao3_api to grab comments from a single fic
### bookmarks.py
- uses ao3_api to bookmark a list of fics (not finished, may not work)
## using [ao3downloader](https://github.com/nianeyna/ao3downloader)
### epub.py
- cli argument style interface for ao3downloader, avoid having to select the same options every time
- use `python epub.py file.txt`
- will log in, not download images separately, only download EPUB format
- run from ao3downloader directory, could not get to login from shell script
### sendlink.py
- download works from ao3 search or collection
- use `python sendlink.py url 2` to download two pages, default one page
- use `python sendlink.py file.txt` to download from first link given
- run from ao3downloader directory, could not get to login from shell script
### id.py
- depends on sendlink.py, needs predefined mega exclude list to download tag search without unwanted fandoms descending kudos or file containing multiple tags
- sample excludelist.txt
- use  `python id.py tag`  tag as in url after `&tag_id=` or use entire url (must sort by kudos descending) 
- i really should fix this one, proof of concept only
- run from ao3downloader directory, could not get to login from shell script
## using [Action Chains](https://www.mobileread.com/forums/showthread.php?t=334974)
### fandommodule.py
- module to identify fandom and set custom column #fandom value to the correct fandom using the Action Chains plugin
### mergemodule.py
- module to automatically merge fanfiction using epubmerge and Action Chains (yes I know fanficfare does this I just want to use ao3downloader)
- doesn't work, couldn't figure out how to call epubmerge from Action Chain, fanficfare does it a different way I think?
![Example of Action Chain configured to set fandom and rating.][actionchainexample]


---

Edit: Not doing this anymore, repurposed the repo.
~~Calibre and ao3downloader provide ways to get metadata in csv format. However, once moved, metadata can be hard to wrangle. I export epubs to a epub reader, many after using epubmerge. The calibre and epub export libraries diverged greatly. I wanted a way to grab metadata locally, without having to request the data again using ao3downloader.~~

library.py contains functions that will export all metadata of epubs in a directory to a csv.
table.py uses NiceGUI to display the table of metadata.
countingtags.py uses ebooklib to count the unsorted tags.

## ~~Roadmap~~

More goals:
- Generate user profile
- Custom Statistics
  - Reading, Date started/Finished
  - Completed
  - Plan to watch
  - Words
  - Subscribed, Kudosed, Bookmarked
  - Author link
  - Series link
- Numerical Ranking
- Tierlists and shelves
  - Fandom
  - Character
  - Pairing
- Sharing
- Reminder to kudos :heart:
- Integrate with Calibre plugin :books:
- Web interface
  - A anilist/myanimelist but for ao3. But ban negative feedback.
