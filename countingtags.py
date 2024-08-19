from collections import Counter
from pathlib import Path
from ebooklib import epub
from bs4 import BeautifulSoup
import json

def extract_subjects(epub_file):
    """Extract all <dc:subject> tags from an EPUB file."""
    try:
        book = epub.read_epub(epub_file)
        subjects = []

        # Extract metadata
        metadata = book.get_metadata('DC', 'subject')

        # Extract <dc:subject> tags from metadata
        for subject in metadata:
            subjects.append(subject[0])
        
        return subjects
    except Exception as e:
        print(f"Error processing {epub_file}: {e}")
        return []

def get_subjects_from_folder(folder_path):
    """Extract and count <dc:subject> tags from all EPUB files in a folder."""
    all_subjects = []

    # Use pathlib to iterate over all EPUB files in the specified folder
    folder = Path(folder_path)
    for epub_file in folder.glob('*.epub'):
        subjects = extract_subjects(epub_file)
        all_subjects.extend(subjects)

    # Count occurrences of each subject
    subject_counter = Counter(all_subjects)

    # Sort subjects by prevalence (most common first)
    sorted_subjects = subject_counter.most_common()

    return sorted_subjects

def testmetadata(epub_path):
    epub_file = Path(epub_path)
    book = epub.read_epub(epub_file)
    print(book.get_metadata('DC', 'subject'))

# Get and print subjects sorted by prevalence
if __name__ == '__main__':
    subjects = get_subjects_from_folder('library/')
    counts = ''
    for subject, count in subjects:
        counts += f"{subject}: {count}"
        counts += '\n'
    test = Path('test.json')
    test.write_text(counts)
