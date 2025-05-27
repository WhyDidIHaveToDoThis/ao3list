from calibre_plugins.action_chains.actions.base import ChainAction
from calibre.library import db

class SetCustomFromTags(ChainAction):
    name = 'Set Custom Column from Tag Rules'

    def run(self, gui, settings, chain):
        db = gui.current_db.new_api
        selected_ids = chain.scope().get_book_ids()
        
        TAG_RULES = {
    'Avatar: The Last Airbender': ['Avatar: The Last Airbender', 'Avatar: Legend of Korra'],
    'Batfamily': ['Batman - All Media Types','Batman (Comics)','DCU - Comicsverse'],
    'Bungou Stray Dogs': ['文豪ストレイドッグス | Bungou Stray Dogs'],
    'Check Please!': ['Check Please! (Webcomic)'],
    'Chronicles of Narnia': ['Chronicles of Narnia - C. S. Lewis'],
    'Dream SMP': ['Dream SMP'],
    'Genshin Impact': ['原神 | Genshin Impact (Video Game)'],
    'Good Omens': ['Good Omens - Neil Gaiman & Terry Pratchett','Good Omens (TV)'],
    'Gravity Falls': ['Gravity Falls'],
    'Hannibal': ['Hannibal (TV)'],
    'Harry Potter': ['Harry Potter - J. K. Rowling','Fantastic Beasts and Where to Find Them (Movies)'],
    'Heartstopper': ['Heartstopper (Webcomic)'],
    'Hockey Bois: A Beer League Romance': ['Hockey Bois: A Beer League Romance'],
    'Hockey RPF': ['Hockey RPF',"Men's Hockey RPF"],
    'How to Train Your Dragon': ['How to Train Your Dragon (Movies)'],
    'Lord of the Rings': ['The Hobbit - All Media Types', 'The Lord of the Rings - All Media Types'],
    'Lunar Chronicles': ['Lunar Chronicles - Marissa Meyer'],
    'Marvel Cinematic Universe': ['Marvel Cinematic Universe','Venom (Movie 2018)','The Avengers (Marvel Movies)','Spider-Man: Homecoming (2017)','Thor (Movies)','Spider-Man - All Media Types','Spider-Man (Tom Holland Movies)','The Avengers (2012)','The Avengers (Marvel) - All Media Types'],
    'Merlin': ['Merlin (TV)','Merlin - Fandom'],
    'Miraculous Ladybug': ['Miraculous Ladybug'],
    'My Little Pony: Friendship is Magic': ['My Little Pony: Friendship is Magic'],
    'Naruto': ['Naruto'],
    'Neon Genesis Evangelion': ['Neon Genesis Evangelion'],
    'Omniscient Reader': ['전지적 독자 시점 - 싱숑 | Omniscient Reader - Sing-Shong'],
    'One Punch Man': ['ワンパンマン | One-Punch Man'],
    'Original Work': ['Original Work'],
    'Parks and Recreation': ['Parks and Recreation'],
    'Percy Jackson': ['Percy Jackson and the Olympians & Related Fandoms - All Media Types','Percy Jackson and the Olympians - Rick Riordan','The Heroes of Olympus - Rick Riordan'],
    'Red White & Royal Blue': ['Red White & Royal Blue - Casey McQuiston'],
    'Rise of the Guardians': ['Rise of the Guardians (2012)'],
    'Scott Pilgrim': ['Scott Pilgrim - All Media Types'],
    'Six of Crows': ['Six of Crows Series - Leigh Bardugo'],
    'Star Trek': ['Star Trek', 'Star Trek: Alternate Original Series (Movies)','Star Trek: Voyager','Star Trek: Prodigy','Star Trek (2009)','Star Trek: Alternate Original Series (Movies)'],
    'Star Wars': ['Star Wars - All Media Types','Star Wars Prequel Trilogy','Star Wars: The Clone Wars (2008) - All Media Types','Star Wars: Rebels','Rogue One: A Star Wars Story (2016)','Solo: A Star Wars Story (2018)','Star Wars Sequel Trilogy','The Mandalorian (TV)', 'Star Wars Original Trilogy','Star Wars: Jedi: Fallen Order Series (Video Games)'],
    'Supernatural': ['Supernatural (TV 2005)','Supernatural'],
    'Tangled': ["Rapunzel's Tangled Adventure (Cartoon)",'Tangled (2010)'],
    'Teen Wolf': ['Teen Wolf (TV)','teen wolf - Fandom'],
    'The Incredibles': ['Incredibles (Pixar Movies)','The Incredibles (2004)'],
    'Twilight': ['Twilight Series - All Media Types'],
    'Unknown': ['PLACEHOLDER'],
    'Voltron: Legendary Defender': ['Voltron: Legendary Defender'],
    'Warriors': ['Warriors - Erin Hunter'],
    'Yuri!!! on Ice': ['Yuri!!! on Ice (Anime)'],
    'Zootopia': ['Zootopia (2016)']
    }

        # Custom Column name, not ID
        CUSTOM_COLUMN = '#fandom'


        for book_id in selected_ids:
            metadata = db.get_metadata(book_id)
            book_tags = set(tag for tag in (metadata.tags or []))

            # Apply tag matching logic
            matched_values = []

            
            for custom_value, trigger_tags in TAG_RULES.items():
                if any(tag in book_tags for tag in trigger_tags):
                	matched_values.append(custom_value)
                	
            if matched_values:
                try:
                    # metadata.set_user_metadata(CUSTOM_COLUMN, ', '.join(matched_values))
                    #db.set_metadata(book_id, metadata)
                    # db.set_custom(book_id, CUSTOM_COLUMN, ', '.join(matched_values))
                    # raise Exception(f'{book_id} {matched_values} {CUSTOM_COLUMN} {metadata} {book_tags}')
                    db.set_field('#fandom', {book_id: ', '.join(matched_values)})
                except:
                    fandomtag = ', '.join(matched_values)
                    raise Exception(f'FAILURE: {book_id} {fandomtag} {CUSTOM_COLUMN} {metadata}')
                    

        gui.library_view.model().refresh_ids(selected_ids)