"""Kobo database backup functionality."""

import json
import shutil
import time
from pathlib import Path

class KoboBackup:
    """Class for backing up Kobo e-reader database."""
    
    DEFAULT_SOURCE_PATH = Path('/Volumes/KOBOeReader/.kobo/KoboReader.sqlite')
    DEFAULT_COOLDOWN = 43200  # 12 hours in seconds
    
    def __init__(self, source_path=None, backup_dir=None, cooldown=None):
        """Initialize the KoboBackup class.
        
        Args:
            source_path (Path, optional): Path to the Kobo database file.
                Defaults to '/Volumes/KOBOeReader/.kobo/KoboReader.sqlite'.
            backup_dir (Path, optional): Directory to store backups.
                Defaults to a 'backups' directory in the package.
            cooldown (int, optional): Cooldown period in seconds.
                Defaults to 12 hours (43200 seconds).
        """
        self.source_file = source_path or self.DEFAULT_SOURCE_PATH
        self.backup_directory = backup_dir if backup_dir else Path(__file__).parent.parent / 'backups'
        self.log_file_path = self.backup_directory / 'backup_log.json'
        self.cooldown_period = cooldown or self.DEFAULT_COOLDOWN
        
        # Ensure backup directory exists
        self.backup_directory.mkdir(parents=True, exist_ok=True)
    
    def initialize_log(self):
        """Initialize the backup log file if it doesn't exist."""
        if not self.log_file_path.exists():
            with self.log_file_path.open('w') as log_file:
                json.dump([], log_file)
    
    def log_backup(self, timestamp, backup_file_name):
        """Log a backup operation.
        
        Args:
            timestamp (str): Timestamp of the backup
            backup_file_name (str): Name of the backup file
        """
        with self.log_file_path.open('r+') as log_file:
            logs = json.load(log_file)
            logs.append({'timestamp': timestamp, 'backup_file': backup_file_name})
            log_file.seek(0)
            log_file.truncate()
            json.dump(logs, log_file, indent=4)
    
    def read_last_backup_time(self):
        """Read the timestamp of the last backup.
        
        Returns:
            float: Unix timestamp of the last backup, or 0 if no backups exist
        """
        if self.log_file_path.exists():
            with self.log_file_path.open('r') as log_file:
                logs = json.load(log_file)
                if logs:
                    return time.mktime(time.strptime(logs[-1]['timestamp'], '%Y%m%d_%H%M%S'))
        return 0
    
    def can_backup(self, last_backup_time):
        """Check if enough time has passed since the last backup.
        
        Args:
            last_backup_time (float): Unix timestamp of the last backup
            
        Returns:
            bool: True if a backup can be performed, False otherwise
        """
        current_time = time.time()
        return (current_time - last_backup_time) > self.cooldown_period
    
    def backup(self):
        """Perform a backup of the Kobo database if conditions are met.
        
        Returns:
            bool: True if backup was successful, False otherwise
        """
        self.initialize_log()
        last_backup_time = self.read_last_backup_time()
        
        if not self.source_file.exists():
            print('Kobo is not connected.')
            return False
            
        if not self.can_backup(last_backup_time):
            print('Backup skipped: within cooldown period.')
            return False
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_file_name = f'KoboReader_{timestamp}.sqlite'
        backup_file_path = self.backup_directory / backup_file_name
        
        try:
            shutil.copy2(self.source_file, backup_file_path)
            print(f'Backup successful: {backup_file_path}')
            self.log_backup(timestamp, backup_file_name)
            return True
        except Exception as e:
            print(f'Error during backup: {e}')
            return False

def backup_kobo_database(source_path=None, backup_dir=None, cooldown=None):
    """Convenience function to backup Kobo database.
    
    Args:
        source_path (Path, optional): Path to the Kobo database file
        backup_dir (Path, optional): Directory to store backups
        cooldown (int, optional): Cooldown period in seconds
        
    Returns:
        bool: True if backup was successful, False otherwise
    """
    backup = KoboBackup(source_path, backup_dir, cooldown)
    return backup.backup()
