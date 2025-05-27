from calibre_plugins.epubmerge.epubmerge_plugin import EpubMergePlugin
from calibre_plugins.epubmerge.epubmerge import doMerge
from calibre_plugins.action_chains.actions.base import ChainAction
from calibre.library import db
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import Dispatcher
from PyQt5.QtWidgets import QAction
import time
import os


class AutoMergeSimple(ChainAction, InterfaceAction):
    name = 'Combine epubs using EpubMerge'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = None  # Will be initialized in the run method
        self.t = time.time()
        self.qaction = None  # We'll initialize this in the run method
        self.Dispatcher = Dispatcher  # Assuming Dispatcher is imported or defined elsewhere
        self.merge_done = EpubMergePlugin.merge_done  # Assign merge_done from EpubMergePlugin
    
    def run(self, gui, settings, chain):
        
        self.qaction = QAction(self.name, self.gui)  
        # Create an action for the UI button

        # Connect the action to a method
        # Now, call a method to start the merge process (or any UI logic)
        
        # self.qaction = QAction(self.name, self.gui)
        # self.t = time.time()
        # self.Dispatcher = Dispatcher
        # self.merge_done = EpubMergePlugin.merge_done
        
        self.gui = gui
        db = gui.current_db.new_api
        selected_ids = chain.scope().get_book_ids()
        
        
        series_dict = {}
        
        for book_id in selected_ids:
            metadata = db.get_metadata(book_id)
            # get series name [Alpha]
            # keys = metadata.standard_field_keys()
            # keys1 = metadata.custom_field_keys()
            # url = db.format_abspath(book_id,'EPUB')
            # size = metadata.size
            # raise Exception(f'test {keys} {url} {keys1} {size}')
            # raise Exception(f'test {comment}')
            book_series = metadata.series
            series_index = int(metadata.series_index)
    
            # If the series is not already in the dictionary, initialize it
            if book_series not in series_dict:
                series_dict[book_series] = []
    
            # Append the new series index to the list for this series
            series_dict[book_series].append((series_index, book_id))
    
            # Sort the dicts by value
            series_dict[book_series].sort()
            
                # raise Exception(f'{book_id} {book_series} {series_dict}')
        error_list = []
        
        for book_series, indexes in series_dict.items():
            indexlist = [index[0] for index in indexes]
            if indexlist == list(range(1, len(indexes) + 1)):
                booklist = [index[1] for index in indexes]
                
                mergeformat = []
                
                for id in booklist:
                    
                    # pathlist.append(db.format_abspath(book_id,'EPUB'))
                    metadata = db.get_metadata(id)
                    
                    # raise Exception(f'{metadata} {metadata.authors} {metadata.author_sort_map} {metadata.size}')
                    
                    book = {}
                    book['good'] = 'good'
                    book['calibre_id'] = id
                    book['title'] = metadata.title
                    book['authors'] = metadata.authors
                    book['author_sort'] = metadata.author_sort_map
                    book['error'] = ''  # No error by default
                    book['comments'] = metadata.comments
                    book['series'] = metadata.series
                    book['series_index'] = int(metadata.series_index)
                    book['publisher'] = metadata.publisher
                    book['pubdate'] = metadata.pubdate
                    book['tags'] = metadata.tags
                    book['languages'] = metadata.languages
                    book['epub'] = db.format_abspath(id,'EPUB')
                    book['epub_size'] = os.stat(book['epub']).st_size
                    mergeformat.append(book)
                
                # pathlist = []
                
                # for id in booklist:
                    # pathlist.append(db.format_abspath(book_id,'EPUB'))
                    # commentmerge.append
                    # comment = (db.get_metadata(id)).
                
                # raise Exception(f'{pathlist} {commentmerge}')
                # raise Exception(f'true {pathlist}')
                # raise Exception(f'true {formats}')
                
                
                # raise Exception(f"{book['epub']}")
                EpubMergePlugin._start_merge(self, book_list=mergeformat, tdir=None)
                # filename = f"{book_series}.epub"
                
                # doMerge(outputio=filename, files=pathlist, titleopt=book_series)
                
                # raise Exception(f'{mergeformat}')
         
            else:
                error_list.append(book_series)
                raise Exception(f'{error_list}')
                
        