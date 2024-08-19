from pathlib import Path
from bs4 import BeautifulSoup
from ebooklib import epub
import ebooklib
import re
import pandas
import json

def fetch_metadata(epub_path):
    """From epub file, get metadata in dict, list format"""

    # Define the path to the EPUB file
    epub_file = Path(epub_path)

    # Load the EPUB file
    book = epub.read_epub(epub_file)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

    # Create metadata
    metadata = {}
    metadata['Path'] = epub_path

    # Parse the first HTML split using BeautifulSoup
    soup = BeautifulSoup(items[0].content, 'html.parser')

    flag = False
    # Get the work url
    ao3 = re.compile(r'archiveofourown\.org\/works\/')
    ao3_url = soup.find('a', {'href': ao3})

    if ao3_url and 'href' in ao3_url.attrs:
        url = ao3_url['href']
        metadata['Link'] = url

        # get the metadata in the epub

        item1 = book.get_metadata('DC', 'description')
        if item1:
            soup1 = BeautifulSoup(item1[0][0], 'html.parser')
            if soup1.prettify().startswith('<p>Anthology containing:</p>'):
                for br in soup1.find_all('br'):
                    br.replace_with(', ')
                description = soup1.get_text(separator=' ', strip=True)
                description = description.replace('Anthology containing: ', '')
                metadata['Anthology'] = description
                flag = True

        item2 = book.get_metadata('DC', 'title')
        if item2:
            soup2 = BeautifulSoup(item2[0][0], 'html.parser')
            title = soup2.get_text()
            metadata['Title'] = title

        # basic metadata parser, will not retain tag separation
        header = soup.find_all('dt')
        data = soup.find_all('dd')
        for h, d in zip(header, data):
            if h.text == 'Stats:':
                
                # text = d.text.strip().split("\n")
                # pairs = dict([x.strip().split(": ") for x in text])
                # metadata.update(pairs)
                metadata.update(dict(x.strip().split(": ") for x in d.text.strip().split("\n")))
                if re.fullmatch(r'\d+\/\d+', metadata.get('Chapters')):
                    if metadata.get('Chapters') == '1/1':
                        metadata['Completed'] = metadata.get('Published')
                    metadata['Updated'] = metadata.get('Completed')

                    
            elif h.text in {'Fandom:','Character:','Archive Warning:','Relationship:'}:
                metadata[h.text.replace(':', 's')] = d.text
            elif h.text == 'Category:':
                metadata[h.text.replace('y:', 'ies')] = d.text
            else:
                dfix = d.text.replace('\n', ' ')
                metadata[h.text.replace(':', '')] = dfix
        # oh wait i also need the second split for the description
        if len(items) > 1:
            soup3 = BeautifulSoup(items[1].content, 'html.parser')
            section = soup3.find('p', string='Summary')
            if section:
                summary = section.find_next_sibling()
                for br in summary.find_all('br'):
                    br.replace_with('\n')
                metadata['Description'] = summary.get_text()
    
        # you also need to fill in the null results?
        # if metadata.get('Fandom') == None:
        #    metadata['Fandom'] = 'WHYY'
        
        return metadata
    else:
        return
    

def create_database(library_path):
    """From directory containing epubs, add to pandas dataframe"""
    library = Path(library_path)
    
    data_list = []
    # content = ''

    for epub in library.glob('*.epub'):
        data = fetch_metadata(epub)
        if data:
            # content += (json.dumps(data,indent=4)) 
            data_list.append(data)
    df = pandas.DataFrame(data_list)
    # test = Path('test.json')
    # test.write_text(content)

    return df

# depricated
def get_desc(epub_path):
    """testing for parts of epub"""
    epub_file = Path(epub_path)
    book = epub.read_epub(epub_file)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    soup = BeautifulSoup(items[1].content, 'html.parser')
    
    section = soup.find('p', string='Summary')
    if section:
        summary = section.find_next_sibling()

    return summary.get_text()


def test_database(library_path):
    """From directory containing epubs, add to pandas dataframe"""
    library = Path(library_path)
    
    data_list = []
    
    for epub in library.glob('*.epub'):
        data = fetch_metadata(epub)
        print(json.dumps(data,indent=4))
        data_list.append(data)
    
    # df = pandas.DataFrame(data_list)
        if data:
            x = input('next?\n')
            if x == 'y':
                print(json.dumps(dict(sorted(data.items())),indent=4))


def test_desc(epub_path):
    """get the metadata description"""
    epub_file = Path(epub_path)
    book = epub.read_epub(epub_file)

    item1 = book.get_metadata('DC', 'description')
    soup1 = BeautifulSoup(item1[0][0], 'html.parser')
    description = soup1.get_text(separator=' ', strip=True)
    description = description.replace('<br/>', ', ')

    item2 = book.get_metadata('DC', 'title')
    soup2 = BeautifulSoup(item2[0][0], 'html.parser')
    title = soup2.get_text()

    """
    for item in book['metadata']:
        # Check if the item is an XML file
        if item.get_type() == epub.EpubHtml:
        # Parse the content with BeautifulSoup
            soup = BeautifulSoup(item.get_body_content(), 'xml')
            
            # Find the <dc:description> tag
            description_tag = soup.find('dc:description', namespace='http://purl.org/dc/elements/1.1/')
            
            if description_tag:
                description = description_tag.get_text()
    """
    return description, title


if __name__ == "__main__":
    try:
        print(json.dumps(fetch_metadata('test.epub'),indent=4))
    except: 
        print('Could not get metadata from test.epub')
    try:
        print(create_database('library/'))
    except:
        print('Could not create pandas dataframe from library directory.')
    try:
        df = create_database('library/')
        df.to_csv('library.csv', index=False)
        print('DONE!')
    except:
        print('Could not export to csv.')


