# Quick Start Guide

## Installation

1. Install the package:

```bash
# Using pip (create a virtual environment first if needed)
pip install -e .

# Or using pipx (recommended for CLI tools)
pipx install .
```

2. Download the required spaCy NLP model:

```bash
python -m spacy download en_core_web_lg
```

This downloads a ~400MB model file needed for name and location detection.

## First Run

1. Initialize your config file:

```bash
scrub --init-config
```

This creates `~/.config/scrub/config.yaml` with example corporate terms.

2. Edit the config file to add your company's information:

```bash
# macOS/Linux
nano ~/.config/scrub/config.yaml
# or
code ~/.config/scrub/config.yaml
```

3. Test it out:

```bash
# Test with stdin
echo "My email is john@acme.com" | scrub --stdin

# Or copy some text and run
pbcopy <<< "My name is John Smith, SSN: 123-45-6789"
scrub
pbpaste
```

## Setting Up Keyboard Shortcut (macOS)

### Option 1: Using Shortcuts.app

1. Open **Shortcuts.app**
2. Click **+** to create new shortcut
3. Add "Run Shell Script" action
4. Enter the full path to scrub:
   ```bash
   /full/path/to/scrub
   # Find your path with: which scrub
   ```
5. Save as "Scrub Clipboard"
6. Right-click → **Add Keyboard Shortcut**
7. Press your desired key combo (e.g., Cmd+Shift+V)

### Finding Your scrub Path

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

## Updating Your Config

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
- Verify `scrub` works from terminal first
- Check the path in your shortcut matches `which scrub`
- macOS may need permissions for Shortcuts/Automator

**Want to install system-wide?**
```bash
# Use pipx (installs in isolated environment)
brew install pipx
pipx install .
```
