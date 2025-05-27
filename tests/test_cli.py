"""Tests for command-line interface."""

import pytest
from click.testing import CliRunner
from pathlib import Path
from unittest.mock import patch

from kobo_utils.cli import cli, backup_command, export_command

@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()

def test_backup_command(runner):
    """Test backup command."""
    with patch('kobo_utils.cli.backup_kobo_database') as mock_backup:
        mock_backup.return_value = True
        
        # Test with explicit source
        result = runner.invoke(backup_command, ['--source', 'test.sqlite'])
        assert result.exit_code == 0
        mock_backup.assert_called_once()
        
        # Check that Path conversion happened
        args = mock_backup.call_args[1]
        assert isinstance(args['source_path'], Path)

def test_export_command(runner):
    """Test export command."""
    with patch('kobo_utils.cli.export_kobo_highlights') as mock_export:
        mock_export.return_value = 5
        
        # Test with required output
        result = runner.invoke(export_command, ['--source', 'test.sqlite', '--output', 'output_dir'])
        assert result.exit_code == 0
        mock_export.assert_called_once()
        
        # Check that Path conversion happened
        args = mock_export.call_args[1]
        assert isinstance(args['db_path'], Path)
        assert isinstance(args['output_folder'], Path)

@patch('kobo_utils.cli.backup_command')
@patch('kobo_utils.cli.export_command')
def test_main_cli(mock_export_cmd, mock_backup_cmd, runner):
    """Test main CLI function."""
    # Test backup command
    result = runner.invoke(cli, ['backup'])
    assert result.exit_code == 0
    
    # Test export command
    result = runner.invoke(cli, ['export', '--output', 'test'])
    assert result.exit_code == 0
