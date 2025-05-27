"""Common utilities for kobo-utils package."""

import os
from pathlib import Path

def find_kobo_device():
    """Find the path to the connected Kobo device.
    
    Returns:
        Path: Path to the Kobo device, or None if not found
    """
    # Common mount points for Kobo devices
    possible_paths = [
        Path('/Volumes/KOBOeReader'),  # macOS
        Path('/media/KOBOeReader'),    # Linux
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

def get_kobo_db_path():
    """Get the path to the Kobo database file.
    
    Returns:
        Path: Path to the Kobo database file, or None if not found
    """
    kobo_path = find_kobo_device()
    if kobo_path:
        db_path = kobo_path / '.kobo' / 'KoboReader.sqlite'
        if db_path.exists():
            return db_path
    
    return None

def normalize_book_title(title):
    """Normalize a book title for use in filenames.
    
    Args:
        title (str): Original book title
        
    Returns:
        str: Normalized book title
    """
    if not title:
        return "Unknown Title"
        
    # Replace characters that are problematic in filenames
    replacements = {
        ':': ' -',
        '/': '-',
        '\\': '-',
        '*': '',
        '?': '',
        '"': "'",
        '<': '',
        '>': '',
        '|': '-'
    }
    
    for char, replacement in replacements.items():
        title = title.replace(char, replacement)
        
    return title.strip()
