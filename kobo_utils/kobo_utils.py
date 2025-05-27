"""Main module."""

import argparse
import sqlite3
from pathlib import Path


class KoboExporter:
    def __init__(self, db_path, output_folder):
        self.db_path = db_path
        self.output_folder = Path(output_folder)
        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True)

    def query_highlights(self):
        query = """
        SELECT
            Bookmark.VolumeID,
            Bookmark.Text,
            Bookmark.Type,
            Bookmark.Annotation,
            Bookmark.DateCreated,
            content.BookTitle,
            content.Title,
            content.Attribution
        FROM Bookmark
        INNER JOIN content ON Bookmark.VolumeID = content.ContentID;
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        highlights = cursor.fetchall()
        cursor.close()
        connection.close()
        return highlights

    def export_highlights(self):
        highlights = self.query_highlights()
        book_counter = {}
        for highlight in highlights:
            (
                volume_id,
                text,
                type_anno,
                annotation,
                date_created,
                book_title,
                title,
                author,
            ) = highlight
            # Normalize the book title to ensure it has a title and to avoid any file naming issues
            # Looking at my DB (Mostly Calibre books), Some books have the book_title in the title field, while others only have title.
            # This isn't "the best" solution, but it works for me at the moment. Will revisit if it breaks.
            # This character replacement works for the books I've tried (~100ish), but should be developed into a comprehensive solution for all invalid characters.
            if book_title is None:
                book_title = title.replace(':', ' -')
            # If this book is encountered for the first time, initialize the counter
            if book_title not in book_counter:
                book_counter[book_title] = 1
            else:
                book_counter[book_title] += 1
            index = book_counter[book_title]
            self.generate_markdown_file(highlight, index, book_title, author)

    def generate_markdown_file(self, highlight, index, book_title, author):
        volume_id, text, type_anno, annotation, date_created, _, title, _ = highlight
        annotation_type = '' if type_anno == 'highlight' else f'{type_anno}'
        filename = f'{book_title} Highlight {index}.md'

        file_path = self.output_folder / book_title / filename

        (self.output_folder / book_title).mkdir(parents=True, exist_ok=True)

        # This is the actual markdown output. An easier to read format can be found in the README.md.
        # If you want your own markdown format for your notes, you can modify the markdown_content variable below.
        # TODO: Move the template into a separate file and import it instead of hardcoding the format.
        # TODO: Write a variety of sample templates and allow users to select one.
        # TODO: Add ability for users to BYOT (Bring Your Own Template) with variable keywords they can use to customize it.
        markdown_content = f"""---
title: "{book_title}"
author: "{author}"
date_created: "{date_created}"
tags: [book-quote, highlight, {annotation_type}]
---
## Reference Text
> {text}
-  {author}, [[{book_title}]]
"""
        # Write to file
        with file_path.open(mode='w', encoding='utf-8') as file:  # Use Path.open() for file writing
            file.write(markdown_content)

def main():
    parser = argparse.ArgumentParser(
        description='Export Kobo highlights to Markdown files',
    )
    parser.add_argument(
        'db', type=str, help='Path to the KoboReader.sqlite database file',
    )
    parser.add_argument(
        'output_directory', type=str, help='Directory to save the Markdown files',
    )
    args = parser.parse_args()
    exporter = KoboExporter(args.db, args.output_directory)
    exporter.export_highlights()
    print(f'Highlights exported to {args.output_directory}')

if __name__ == '__main__':
    main()
