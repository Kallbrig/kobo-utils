# kobo-utils

[![image](https://img.shields.io/pypi/v/kobo-utils.svg)](https://pypi.python.org/pypi/kobo-utils)
[![image](https://img.shields.io/conda/vn/conda-forge/kobo-utils.svg)](https://anaconda.org/conda-forge/kobo-utils)

A collection of tools to help manage and interact with Kobo e-readers.

## Features

- **Database Backup**: Automatically backup your Kobo database with a cooldown period
- **Export Highlights**: Extract highlights from your Kobo and save them as Markdown files (meant for Obsidian at the moment).
- **Organized Output**: Save each book's highlights in a dedicated folder.

## Documentation
 https://kallbrig.github.io/kobo-utils

## Installation

```bash
# Install from PyPI
pip install kobo-utils

# Development installation
git clone https://github.com/kallbrig/kobo-utils.git
cd kobo-utils
pip install -e .
```

## Usage

### Command Line Interface

The package provides two commands for the time being:

#### Backup Kobo Database

```bash
# Basic usage (auto-detects Kobo device)
kobo-utils backup

# Specify custom paths and options
kobo-utils backup --source /path/to/KoboReader.sqlite --output /path/to/backups --cooldown 43200
```

#### Export Kobo Highlights

```bash
# Basic usage (auto-detects Kobo device)
kobo-utils export --output /path/to/highlights

# Specify custom database path
kobo-utils export --source /path/to/KoboReader.sqlite --output /path/to/highlights
```

### Python API

You can also use the package programmatically:

```python
from kobo_utils import backup_kobo_database, export_kobo_highlights
from pathlib import Path

# Backup the Kobo database
backup_kobo_database(
    source_path=Path('/path/to/KoboReader.sqlite'),  # Optional
    backup_dir=Path('/path/to/backups'),             # Optional
    cooldown=43200                                   # Optional, in seconds
)

# Export highlights
export_kobo_highlights(
    db_path=Path('/path/to/KoboReader.sqlite'),      # Optional
    output_folder=Path('/path/to/highlights')        # Required
)
```

## Output Note Format

Each highlight is saved as a separate Markdown file with the following format:

```markdown
---
title: "Book Title"
author: "Author Name"
date_created: "2025-01-01T12:00:00"
tags: [book-quote, highlight]
---
## Reference Text
> This is the highlighted text from the book.
- Author Name, [[Book Title]]
```

This format is designed to work with [Obsidian](https://obsidian.md/) and the [Obsidian-Dataview](https://github.com/blacksmithgu/obsidian-dataview) plugin.

## Requirements

- Python 3.8 or higher
- Click 8.0 or higher

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the Kobo for not being terrible.
- [Obsidian](https://obsidian.md/). It's great. Use it.
- This is a rework of [this repository by Pettarin](https://github.com/pettarin/export-kobo). I just used it for ideas and understanding the structure and then built my own thing. Thanks @Pettarin!
