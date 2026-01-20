"""Command-line interface for scrub tool."""

import sys
from pathlib import Path

import click

from . import __version__
from .clipboard import ClipboardError, read_clipboard, write_clipboard
from .config import Config, create_example_config, get_default_config_path
from .scrubber import TextScrubber


@click.command()
@click.option(
    "--stdin",
    is_flag=True,
    help="Read from stdin instead of clipboard, output to stdout.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be redacted without modifying clipboard.",
)
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Path to config file (default: ~/.config/scrub/config.yaml).",
)
@click.option(
    "--init-config",
    is_flag=True,
    help="Create example config file at default location.",
)
@click.version_option(version=__version__, prog_name="scrub")
def main(stdin: bool, dry_run: bool, config: Path, init_config: bool):
    """
    Scrub PII and corporate information from clipboard or stdin.
    
    By default, reads from clipboard, scrubs the content, and writes back to clipboard.
    
    Examples:
    
        scrub                    # Scrub clipboard in-place
        
        scrub --stdin            # Read from stdin, output to stdout
        
        scrub --dry-run          # Show what would be redacted
        
        scrub --init-config      # Create example config file
    """
    try:
        # Handle init-config flag
        if init_config:
            config_path = get_default_config_path()
            if config_path.exists():
                click.echo(f"Config file already exists at: {config_path}", err=True)
                click.echo("Edit it manually or delete it to create a new one.", err=True)
                sys.exit(1)
            
            create_example_config()
            click.echo(f"Created example config at: {config_path}", err=True)
            click.echo("Edit this file to add your corporate terms.", err=True)
            sys.exit(0)
        
        # Load configuration
        cfg = Config.load(config)
        
        # Create scrubber
        scrubber = TextScrubber(config=cfg)
        
        # Get input text
        if stdin:
            text = sys.stdin.read()
        else:
            try:
                text = read_clipboard()
            except ClipboardError as e:
                click.echo(f"Error reading clipboard: {e}", err=True)
                sys.exit(1)
        
        # Handle empty input
        if not text or not text.strip():
            if not stdin:
                click.echo("Clipboard is empty.", err=True)
            sys.exit(0)
        
        # Dry-run mode: show what would be detected
        if dry_run:
            results = scrubber.analyze(text)
            
            if not results:
                click.echo("No PII or sensitive information detected.", err=True)
                sys.exit(0)
            
            click.echo(f"Found {len(results)} item(s) to redact:", err=True)
            for result in results:
                entity_text = text[result.start:result.end]
                click.echo(
                    f"  - {result.entity_type}: '{entity_text}' "
                    f"(score: {result.score:.2f})",
                    err=True,
                )
            sys.exit(0)
        
        # Scrub the text
        scrubbed_text = scrubber.scrub(text)
        
        # Output
        if stdin:
            # Write to stdout
            click.echo(scrubbed_text)
        else:
            # Write back to clipboard
            try:
                write_clipboard(scrubbed_text)
                # Optionally show success message to stderr
                # click.echo("Clipboard scrubbed successfully.", err=True)
            except ClipboardError as e:
                click.echo(f"Error writing to clipboard: {e}", err=True)
                sys.exit(1)
    
    except KeyboardInterrupt:
        click.echo("\nAborted.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
