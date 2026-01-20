# Keyboard Shortcut Setup Guide - Step by Step

## Method 1: Using Shortcuts.app (Recommended for macOS Monterey+)

### Step-by-Step Instructions:

1. **Shortcuts.app is opened**
   - Press `Cmd+Space` and type "Shortcuts"
   - Or find it in the Applications folder

2. **A New Shortcut is Created**
   - Click the **"+"** button in the top toolbar (or top-right corner)
   - This creates a new blank shortcut

3. **The Shell Script Action is Added**
   - In the search bar on the right side, type: **"Run Shell Script"**
   - Click or drag **"Run Shell Script"** into the workflow area

4. **Configuration of the Script**
   - In the script box that appears, DELETE any existing text
   - Type or paste this EXACT path:
     ```
     ~/.local/bin/scrub
     ```
   - Ensure there are NO extra spaces or quotes

5. **Naming the Shortcut**
   - At the top of the screen, locate "New Shortcut" or similar
   - Click on it and rename to: **"Scrub Clipboard"**

6. **Adding a Keyboard Shortcut**
   
   **IMPORTANT:** The keyboard shortcut option is NOT in Shortcuts.app itself!
   
   The following steps are required:
   - **Save/Close** the shortcut first (it auto-saves)
   - Go to **System Settings** (or System Preferences on older macOS)
   - Go to **Keyboard**
   - Click **Keyboard Shortcuts** (left sidebar)
   - Click **Services** in the left list
   - Scroll down in the right panel to find **"Scrub Clipboard"** under "General"
   - Click on "Scrub Clipboard" - a button should appear on the right
   - Click **"Add Shortcut"** button
   - Press the desired key combination (e.g., `Cmd+Shift+V`)

---

## Method 2: Using Automator (Works on ALL macOS versions)

This method is more reliable and works on older macOS versions:

### Step-by-Step Instructions:

1. **Automator is opened**
   - Press `Cmd+Space` and type "Automator"
   - Or find it in the Applications folder

2. **A Quick Action is Created**
   - Click **"New Document"** (or File → New)
   - Choose **"Quick Action"** (or "Service" on older macOS)
   - Click **Choose**

3. **Configuration of the Workflow**
   - At the top, set:
     - **"Workflow receives:"** → select **"no input"**
     - **"in"** → select **"any application"**

4. **Add Shell Script Action**
   - In the search box (left side), type: **"Run Shell Script"**
   - Double-click **"Run Shell Script"** or drag it to the right panel

5. **Configuration of the Script**
   - In the script text box, DELETE any existing text
   - Type or paste:
     ```
     ~/.local/bin/scrub
     ```
   - Ensure **Shell:** is set to **/bin/bash** or **/bin/zsh**

6. **Saving the Quick Action**
   - Press `Cmd+S` or File → Save
   - Name it: **"Scrub Clipboard"**
   - Click **Save**

7. **Assigning a Keyboard Shortcut**
   - Open **System Settings** (or System Preferences)
   - Go to **Keyboard**
   - Click **Keyboard Shortcuts** (or just "Shortcuts")
   - Click **Services** in the left sidebar
   - Scroll down to find **"Scrub Clipboard"** under "General"
   - Check the checkbox next to it to enable it
   - Click on the right side of "Scrub Clipboard" to add shortcut
   - Press the desired keys (e.g., `Cmd+Shift+V` or `Ctrl+Shift+S`)

---

## Method 3: Simple Alfred/Raycast Alternative

If **Alfred** or **Raycast** is used:

### Alfred:
1. Create a workflow
2. Add a hotkey trigger
3. Connect to a "Run Script" action with:
   ```bash
   ~/.local/bin/scrub
   ```

### Raycast:
1. Create a script command
2. Add the script:
   ```bash
   #!/bin/bash
   ~/.local/bin/scrub
   ```

---

## Recommended Keyboard Shortcuts

A non-conflicting shortcut should be chosen:

- `Cmd+Shift+V` - Similar to "paste without formatting"
- `Ctrl+Shift+S` - Easy to remember (S for Scrub)
- `Cmd+Option+V` - Alternative paste shortcut
- `Ctrl+Option+C` - After copying

**Test if shortcut is taken:** Try pressing it in any application first!

---

## Testing the Shortcut

1. Copy some text with PII:
   ```
   echo "My name is John Smith, email: john@test.com" | pbcopy
   ```

2. Press the keyboard shortcut

3. Paste somewhere (Cmd+V):
   ```
   Should see: My name is <PERSON>, email: <EMAIL_ADDRESS>
   ```

---

## Troubleshooting

### "Shortcut didn't work"
- Ensure it is enabled in System Settings → Keyboard → Shortcuts → Services
- Check the checkbox next to "Scrub Clipboard"
- Try the shortcut again

### "Can't find Scrub Clipboard in Services"
- Close and reopen System Settings
- Log out and log back in
- Restart the Mac

### "Permission denied" errors
- System Settings → Privacy & Security → Automation
- Allow Shortcuts or Automator to control Terminal/System Events

### "Still not working"
- Test manually first: Open Terminal and run `scrub --version`
- Ensure the path is EXACTLY: `~/.local/bin/scrub`
- No quotes, no extra spaces

---

## Quick Manual Test

Before setting up the shortcut, testing is recommended:

```bash
# Copy something
echo "Test: Bob Jones, SSN 123-45-6789" | pbcopy

# Run scrub manually
~/.local/bin/scrub

# Paste to check
pbpaste
# Should show: Test: <PERSON>, <ORGANIZATION> 123-45-6789
```

If this works, the shortcut should work too!

---

## Further Assistance

If issues persist:
1. Check the macOS version (run: `sw_vers`)
2. Note which method was tried (Shortcuts.app or Automator)
3. Observe what happens when the keyboard shortcut is pressed

This information will assist in debugging!
