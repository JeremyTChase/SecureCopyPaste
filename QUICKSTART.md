# Quick Start Guide

## Installation

1. The package is installed:

```bash
# Using pip (create a virtual environment first if needed)
pip install -e .

# Or using pipx (recommended for CLI tools)
pipx install .
```

2. The required spaCy NLP model must be downloaded:

```bash
python -m spacy download en_core_web_lg
```

This downloads a ~400MB model file needed for name and location detection.

## First Run

1. Initialisation of the config file:

```bash
scrub --init-config
```

This creates `~/.config/scrub/config.yaml` with example corporate terms.

2. The config file can be edited to add company information:

```bash
# macOS/Linux
nano ~/.config/scrub/config.yaml
# or
code ~/.config/scrub/config.yaml
```

3. Testing:

```bash
# Test with stdin
echo "My email is john@acme.com" | scrub --stdin

# Or copy some text and run
pbcopy <<< "My name is John Smith, SSN: 123-45-6789"
scrub
pbpaste
```

## Setting Up a Keyboard Shortcut (macOS)

### Option 1: Using Shortcuts.app

1. Shortcuts.app is opened.
2. A new shortcut is created by clicking **+**.
3. A "Run Shell Script" action is added.
4. The full path to `scrub` is entered:
   ```bash
   /full/path/to/scrub
   # Find the path with: which scrub
   ```
5. Saved as "Scrub Clipboard".
6. Right-click → **Add Keyboard Shortcut**.
7. The desired key combination is pressed (e.g., Cmd+Shift+V).

### Finding the `scrub` Path

```bash
which scrub
# Example output: /Users/yourname/.local/bin/scrub (if using pipx)
# Or: /path/to/venv/bin/scrub (if using venv)
```

## Examples

```bash
# Basic usage - scrub clipboard in-place
scrub

# See what would be redacted without changing clipboard
scrub --dry-run

# Process stdin/stdout (for piping)
cat file.txt | scrub --stdin > cleaned.txt

# Use custom config
scrub --config /path/to/custom-config.yaml
```

## Updating the Configuration

Edit `~/.config/scrub/config.yaml`:

```yaml
corporate:
  company_names:
    - "Your Company Name"
    - "YourCo"
  
  domains:
    - "yourcompany.com"
    - "internal.yourco.io"
  
  project_names:
    - "Secret Project"
    - "Product Codename"
  
  deny_list:
    - "proprietary-term"
    - "internal-system-xyz"
```

## Troubleshooting

**spaCy model not found?**
```bash
python -m spacy download en_core_web_lg
```

**Keyboard shortcut not working?**
- Verify `scrub` works from the terminal first
- Check the path in the shortcut matches `which scrub`
- macOS may need permissions for Shortcuts/Automator

**Want to install system-wide?**
```bash
# Use pipx (installs in isolated environment)
brew install pipx
pipx install .
```
