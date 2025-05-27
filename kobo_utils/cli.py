"""Command-line interface for kobo-utils."""

import click
from pathlib import Path

from kobo_utils.backup import backup_kobo_database
from kobo_utils.export import export_kobo_highlights
from kobo_utils.common import get_kobo_db_path

@click.group()
def cli():
    """Kobo e-reader utilities."""
    pass

@cli.command('backup')
@click.option('--source', '-s', type=click.Path(exists=False), 
              help='Path to the KoboReader.sqlite database file (default: auto-detect)')
@click.option('--output', '-o', type=click.Path(), 
              help='Directory to save the backup (default: ./backups)')
@click.option('--cooldown', '-c', type=int, default=12,
              help='Cooldown period in hours (default: 12)')
def backup_command(source, output, cooldown):
    """Backup Kobo e-reader database."""
    # Convert cooldown from hours to seconds
    cooldown_seconds = cooldown * 3600
    
    # Auto-detect Kobo if source not provided
    source_path = source
    if not source_path:
        detected_path = get_kobo_db_path()
        if detected_path:
            source_path = detected_path
        else:
            click.echo("Error: Kobo device not found. Please connect your Kobo or specify the database path with --source.")
            return 1
    
    # Convert string paths to Path objects
    source_path = Path(source_path)
    output_path = Path(output) if output else None
    
    success = backup_kobo_database(
        source_path=source_path,
        backup_dir=output_path,
        cooldown=cooldown_seconds
    )
    
    return 0 if success else 1

@cli.command('export')
@click.option('--source', '-s', type=click.Path(exists=False),
              help='Path to the KoboReader.sqlite database file (default: auto-detect)')
@click.option('--output', '-o', type=click.Path(), required=True,
              help='Directory to save the Markdown files')
def export_command(source, output):
    """Export Kobo highlights to Markdown files."""
    # Auto-detect Kobo if source not provided
    source_path = source
    if not source_path:
        detected_path = get_kobo_db_path()
        if detected_path:
            source_path = detected_path
        else:
            click.echo("Error: Kobo device not found. Please connect your Kobo or specify the database path with --source.")
            return 1
    
    # Convert string paths to Path objects
    source_path = Path(source_path)
    output_path = Path(output)
    
    try:
        count = export_kobo_highlights(
            db_path=source_path,
            output_folder=output_path
        )
        click.echo(f"Successfully exported {count} highlights to {output}")
        return 0
    except Exception as e:
        click.echo(f"Error exporting highlights: {e}")
        return 1

def main():
    """Main entry point for the kobo-utils CLI."""
    return cli()

if __name__ == "__main__":
    main()
