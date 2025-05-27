"""Tests for backup functionality."""

import json
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open

from kobo_utils.backup import KoboBackup

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

def test_initialize_log(temp_dir):
    """Test log initialization."""
    backup = KoboBackup(backup_dir=temp_dir)
    backup.initialize_log()
    assert backup.log_file_path.exists()
    
    with backup.log_file_path.open() as f:
        logs = json.load(f)
        assert logs == []

def test_log_backup(temp_dir):
    """Test logging a backup."""
    backup = KoboBackup(backup_dir=temp_dir)
    backup.initialize_log()
    
    backup.log_backup("20250101_120000", "test_backup.sqlite")
    
    with backup.log_file_path.open() as f:
        logs = json.load(f)
        assert len(logs) == 1
        assert logs[0]["timestamp"] == "20250101_120000"
        assert logs[0]["backup_file"] == "test_backup.sqlite"

@patch('pathlib.Path.exists')
@patch('shutil.copy2')
def test_backup_success(mock_copy, mock_exists, temp_dir):
    """Test successful backup."""
    mock_exists.return_value = True
    
    backup = KoboBackup(backup_dir=temp_dir)
    
    # Mock the log file to return 0 as last backup time
    with patch.object(backup, 'read_last_backup_time', return_value=0):
        with patch.object(backup, 'log_backup'):
            result = backup.backup()
            
    assert result is True
    mock_copy.assert_called_once()

@patch('pathlib.Path.exists')
def test_backup_no_device(mock_exists, temp_dir):
    """Test backup when device is not connected."""
    mock_exists.return_value = False
    
    backup = KoboBackup(backup_dir=temp_dir)
    result = backup.backup()
    
    assert result is False
