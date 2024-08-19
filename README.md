# Catalog fanfiction!
---

Calibre and ao3downloader provide ways to get metadata in csv format. However, once moved, metadata can be hard to wrangle.
I export epubs to a epub reader, many after using epubmerge. The calibre and epub export libraries diverged greatly.
I wanted a way to grab metadata locally, without having to request the data again using ao3downloader.

library.py contains functions that will export all metadata of epubs in a directory to a csv.
table.py uses NiceGUI to display the table of metadata.
countingtags.py uses ebooklib to count the unsorted tags.


## Roadmap

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
