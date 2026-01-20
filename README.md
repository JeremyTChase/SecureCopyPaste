# SecureCopyPaste - `scrub`

A CLI tool to automatically strip PII (Personally Identifiable Information) and corporate information from your clipboard content before pasting.

Built with [Microsoft Presidio](https://microsoft.github.io/presidio/) for robust PII detection and anonymization.

## Features

- Detects and redacts common PII:
  - Names, email addresses, phone numbers
  - Credit cards, SSNs, passports, driver licenses
  - IP addresses, URLs, dates
  - Medical licenses, bank account numbers
  - And much more (see [supported entities](https://microsoft.github.io/presidio/supported_entities/))

- Custom corporate information redaction:
  - Company/organization names
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

### Install Steps

1. Clone or download this repository:

```bash
cd ~/Github/SecureCopyPaste
```

2. Install the package:

```bash
# Install in development mode (recommended for easy updates)
pip install -e .

# Or install normally
pip install .
```

3. Download the spaCy NLP model (required for name/location detection):

```bash
python -m spacy download en_core_web_lg
```

This may take a few minutes as the model is ~500MB.

4. (Optional) Create a configuration file:

```bash
scrub --init-config
```

This creates `~/.config/scrub/config.yaml` with example corporate terms. Edit this file to add your own company names, domains, project names, and deny-list terms.

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

The config file at `~/.config/scrub/config.yaml` allows you to specify corporate information to redact:

```yaml
corporate:
  # Company/organization names
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

See `config/config.example.yaml` for a complete example.

## macOS Keyboard Shortcut Setup

For quick access, set up a keyboard shortcut to run `scrub` automatically.

### Option 1: Using macOS Shortcuts.app (Recommended)

1. Open **Shortcuts.app** (comes with macOS)

2. Click the **+** button to create a new shortcut

3. Add a "Run Shell Script" action:
   - Search for "Run Shell Script" in the actions sidebar
   - Drag it to the workflow

4. Configure the shell script:
   - Shell: `/bin/bash`
   - Pass input: (doesn't matter)
   - Script content:
     ```bash
     /usr/local/bin/scrub
     ```
   
   Note: Find your `scrub` path with: `which scrub`

5. Save the shortcut with a name like "Scrub Clipboard"

6. Assign a keyboard shortcut:
   - Right-click the shortcut → **Add Keyboard Shortcut**
   - Press your desired key combination (e.g., `Cmd+Shift+V` or `Ctrl+Shift+S`)
   - If the shortcut is already in use, try another combination

7. Test it:
   - Copy some text with PII to your clipboard
   - Press your keyboard shortcut
   - Paste to verify the content was scrubbed

### Option 2: Using Automator

1. Open **Automator** (in Applications)

2. Create a new **Quick Action**

3. Configure the workflow:
   - "Workflow receives": **no input** in **any application**
   - Add action: **Run Shell Script**
   - Shell: `/bin/bash`
   - Pass input: **as arguments**
   - Script:
     ```bash
     /usr/local/bin/scrub
     ```

4. Save as "Scrub Clipboard"

5. Assign keyboard shortcut:
   - Open **System Settings** → **Keyboard** → **Shortcuts**
   - Select **Services** in the sidebar
   - Find "Scrub Clipboard" under **General**
   - Click **Add Shortcut** and press your desired keys

### Warp Terminal Integration

Since you're using Warp, you can also create an alias or function in your shell profile:

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
        └── recognizers/        # Custom PII recognizers
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

Make sure you downloaded the model:

```bash
python -m spacy download en_core_web_lg
```

### No PII detected

Presidio uses confidence scores. Some entities may not be detected if:
- The confidence score is too low
- The text doesn't match expected patterns
- The NLP model doesn't recognize the entity

You can use `--dry-run` to see what is detected.

### Keyboard shortcut not working

- Make sure the `scrub` command works from terminal first
- Verify the path to `scrub` in your shortcut matches `which scrub`
- Check that the keyboard shortcut isn't already in use
- macOS may require permissions for Shortcuts/Automator to run shell commands

## Security Notes

- Presidio uses automated detection and may not catch all PII
- Always review scrubbed content before sharing sensitive information
- Consider this tool as a helpful safeguard, not a guarantee
- Config files may contain sensitive corporate terms - protect accordingly

## License

MIT

## Acknowledgments

- Built with [Microsoft Presidio](https://microsoft.github.io/presidio/)
- Uses [spaCy](https://spacy.io/) for NLP
