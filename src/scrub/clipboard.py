"""macOS clipboard utilities using pbcopy/pbpaste."""

import subprocess
from typing import Optional


class ClipboardError(Exception):
    """Raised when clipboard operations fail."""
    pass


def read_clipboard() -> str:
    """
    Read text content from macOS clipboard.
    
    Returns:
        str: The clipboard content as text.
        
    Raises:
        ClipboardError: If reading from clipboard fails.
    """
    try:
        result = subprocess.run(
            ["pbpaste"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise ClipboardError(f"Failed to read clipboard: {e}") from e
    except FileNotFoundError:
        raise ClipboardError(
            "pbpaste command not found. This tool requires macOS."
        ) from None


def write_clipboard(text: str) -> None:
    """
    Write text content to macOS clipboard.
    
    Args:
        text: The text to write to clipboard.
        
    Raises:
        ClipboardError: If writing to clipboard fails.
    """
    try:
        subprocess.run(
            ["pbcopy"],
            input=text,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise ClipboardError(f"Failed to write clipboard: {e}") from e
    except FileNotFoundError:
        raise ClipboardError(
            "pbcopy command not found. This tool requires macOS."
        ) from None
