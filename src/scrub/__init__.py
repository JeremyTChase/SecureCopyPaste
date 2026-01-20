"""scrub - CLI tool to strip PII and corporate information from clipboard content."""

__version__ = "0.1.0"

from .clipboard import read_clipboard, write_clipboard
from .config import Config
from .scrubber import TextScrubber, scrub_text

__all__ = [
    "Config",
    "TextScrubber",
    "scrub_text",
    "read_clipboard",
    "write_clipboard",
]
