"""Tests for export functionality."""

import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from kobo_utils.export import KoboExporter

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def sample_highlight():
    """Create a sample highlight for testing."""
    return (
        "_volume_",            # VolumeID
        "_highlight_",         # Actual Highlight Text
        "highlight",           # Type
        None,                  # Annotation
        "2025-01-01T12:00:00", # DateCreated
        "Test Book",           # BookTitle
        "Test Book",           # Title
        "Test Author"          # Author
    )

@patch('sqlite3.connect')
def test_query_highlights(mock_connect, temp_dir):
    """Test querying highlights from the database."""
    # Set up mock cursor and connection
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    
    # Set up mock fetchall to return sample data
    mock_cursor.fetchall.return_value = [
        ("_volume_", "_highlight_", "highlight", None, 
         "2025-01-01T12:00:00", "Test Book", "Test Book", "Test Author")
    ]
    
    exporter = KoboExporter(db_path=Path("test.sqlite"), output_folder=temp_dir)
    highlights = exporter.query_highlights()
    
    assert len(highlights) == 1
    assert highlights[0][0] == "_volume_"
    assert highlights[0][1] == "_highlight_"

def test_generate_markdown_file(temp_dir, sample_highlight):
    """Test generating a markdown file for a highlight."""
    exporter = KoboExporter(output_folder=temp_dir)
    
    exporter.generate_markdown_file(
        highlight=sample_highlight,
        index=1,
        book_title="Test Book",
        author="Test Author"
    )
    
    # Check if the file was created
    expected_path = temp_dir / "Test Book" / "Test Book Highlight 1.md"
    assert expected_path.exists()
    

    content = expected_path.read_text()
    assert 'title: "Test Book"' in content
    assert 'author: "Test Author"' in content
    assert '> _highlight_' in content

@patch.object(KoboExporter, 'query_highlights')
def test_export_highlights(mock_query, temp_dir, sample_highlight):
    """Test exporting all highlights."""
    mock_query.return_value = [sample_highlight]
    
    exporter = KoboExporter(output_folder=temp_dir)
    
    with patch.object(exporter, 'generate_markdown_file') as mock_generate:
        count = exporter.export_highlights()
        
    assert count == 1
    mock_generate.assert_called_once()
