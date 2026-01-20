# SecureCopyPaste - `scrub`

A CLI tool to automatically strip PII (Personally Identifiable Information) and corporate information from clipboard content before pasting.

Built with [Microsoft Presidio](https://microsoft.github.io/presidio/) for robust PII detection and anonymisation.

## Features

- Detects and redacts common PII:
  - Names, email addresses, phone numbers
  - Credit cards, SSNs, passports, driver licences
  - IP addresses, URLs, dates
  - Medical licences, bank account numbers
  - And much more (see [supported entities](https://microsoft.github.io/presidio/supported_entities/))

- Custom corporate information redaction:
  - Company/organisation names
  - Internal domains and URLs
  - Project/product code names
  - Custom deny-list terms

- Multiple usage modes:
  - CLI command for manual scrubbing
  - macOS keyboard shortcut for quick access
  - Pipe mode for integration with other tools

## Installation

### Prerequisites

- Python 3.8 or higher
- macOS (uses `pbcopy`/`pbpaste` for clipboard access)

### Installation Steps

1. The repository can be cloned or downloaded:

```bash
cd ~/Github/SecureCopyPaste
```

2. The package is then installed:

```bash
# Install in development mode (recommended for easy updates)
pip install -e .

# Or install normally
pip install .
```

3. The spaCy NLP model must be downloaded (required for name/location detection):

```bash
python -m spacy download en_core_web_lg
```

This may take a few minutes as the model is ~500MB.

4. (Optional) A configuration file can be created:

```bash
scrub --init-config
```

This creates `~/.config/scrub/config.yaml` with example corporate terms. This file can be edited to include company names, domains, project names, and deny-list terms.

## Usage

### Basic CLI Usage

```bash
# Scrub clipboard in-place (reads clipboard, scrubs, writes back)
scrub

# Read from stdin, output to stdout
echo "Call John Doe at 555-1234" | scrub --stdin
# Output: Call <PERSON> at <PHONE_NUMBER>

# Dry-run: see what would be redacted without modifying clipboard
scrub --dry-run

# Use custom config file
scrub --config /path/to/config.yaml

# Show version
scrub --version
```

### Example

Input (clipboard):
```
Hi, I'm Jane Smith from Acme Corp. 
Email me at jane.smith@acme.com or call 555-123-4567.
Our internal system is at https://internal.acme.io
Credit card: 4532-1488-0343-6467
```

After running `scrub`:
```
Hi, I'm <PERSON> from <CORPORATE_NAME>. 
Email me at <EMAIL_ADDRESS> or call <PHONE_NUMBER>.
Our internal system is at <INTERNAL_DOMAIN>
Credit card: <CREDIT_CARD>
```

### Configuration

The config file at `~/.config/scrub/config.yaml` allows for the specification of corporate information to redact:

```yaml
corporate:
  # Company/organisation names
  company_names:
    - "Acme Corp"
    - "Acme Inc"
  
  # Internal domains (matches in URLs and emails)
  domains:
    - "acme.com"
    - "internal.acme.io"
  
  # Project/product code names
  project_names:
    - "Project Phoenix"
    - "Codename Titan"
  
  # Custom terms to always redact
  deny_list:
    - "confidential-system-name"
    - "internal-tool-v2"
```

A complete example is available in `config/config.example.yaml`.

## macOS Keyboard Shortcut Setup

For quick access, a keyboard shortcut can be set up to run `scrub` automatically.

### Option 1: Using macOS Shortcuts.app (Recommended)

1. Shortcuts.app can be opened (comes with macOS).

2. A new shortcut is created by clicking the **+** button.

3. A "Run Shell Script" action is added:
   - Search for "Run Shell Script" in the actions sidebar
   - Drag it to the workflow

4. The shell script is configured as follows:
   - Shell: `/bin/bash`
   - Pass input: (doesn't matter)
   - Script content:
     ```bash
     /usr/local/bin/scrub
     ```
   
   Note: The `scrub` path can be found with: `which scrub`

5. The shortcut is saved with a name like "Scrub Clipboard".

6. A keyboard shortcut is assigned:
   - Right-click the shortcut → **Add Keyboard Shortcut**
   - Press the desired key combination (e.g., `Cmd+Shift+V` or `Ctrl+Shift+S`)
   - Ensure the shortcut is not already in use by another application.

7. Testing:
   - Copy text with PII to the clipboard
   - Press the keyboard shortcut
   - Paste to verify the content was scrubbed

### Option 2: Using Automator

1. Automator (in Applications) is opened.

2. A new **Quick Action** is created.

3. The workflow is configured:
   - "Workflow receives": **no input** in **any application**
   - Add action: **Run Shell Script**
   - Shell: `/bin/bash`
   - Pass input: **as arguments**
   - Script:
     ```bash
     /usr/local/bin/scrub
     ```

4. Saved as "Scrub Clipboard".

5. A keyboard shortcut is assigned:
   - Open **System Settings** → **Keyboard** → **Shortcuts**
   - Select **Services** in the sidebar
   - Find "Scrub Clipboard" under **General**
   - Click **Add Shortcut** and press the desired keys

### Warp Terminal Integration

For Warp users, an alias or function can be created in the shell profile:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias scrub-clip='scrub'

# Or create a function that shows a notification
function scrub-clip() {
    scrub && echo "✓ Clipboard scrubbed"
}
```

## Development

### Project Structure

```
SecureCopyPaste/
├── pyproject.toml              # Project metadata and dependencies
├── README.md                   # This file
├── config/
│   └── config.example.yaml     # Example configuration
└── src/
    └── scrub/
        ├── __init__.py         # Package init
        ├── cli.py              # CLI entry point
        ├── clipboard.py        # macOS clipboard utilities
        ├── config.py           # Configuration management
        ├── scrubber.py         # Core Presidio integration
        └── recognisers/        # Custom PII recognisers
            ├── corporate.py    # Company name detection
            ├── domains.py      # Internal domain detection
            └── denylist.py     # Custom deny-list terms
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests (when available)
pytest
```

## Troubleshooting

### `pbpaste` or `pbcopy` not found

This tool requires macOS. The clipboard commands are macOS-specific.

### spaCy model not found

Ensure the model has been downloaded:

```bash
python -m spacy download en_core_web_lg
```

### No PII detected

Presidio uses confidence scores. Some entities may not be detected if:
- The confidence score is too low
- The text doesn't match expected patterns
- The NLP model doesn't recognise the entity

Use `--dry-run` to see what is detected.

### Keyboard shortcut not working

- Ensure the `scrub` command works from the terminal first
- Verify the path to `scrub` in the shortcut matches `which scrub`
- Check that the keyboard shortcut isn't already in use
- macOS may require permissions for Shortcuts/Automator to run shell commands

## Security Notes

- Presidio uses automated detection and may not catch all PII
- Scrubbed content should always be reviewed before sharing sensitive information
- This tool serves as a helpful safeguard, not a guarantee
- Config files may contain sensitive corporate terms - protect accordingly

## Licence

MIT

## Acknowledgments

- Built with [Microsoft Presidio](https://microsoft.github.io/presidio/)
- Uses [spaCy](https://spacy.io/) for NLP
