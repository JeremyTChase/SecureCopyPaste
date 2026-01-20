# Keyboard Shortcut Setup Guide - Step by Step

## Method 1: Using Shortcuts.app (Recommended for macOS Monterey+)

### Step-by-Step Instructions:

1. **Open Shortcuts.app**
   - Press `Cmd+Space` and type "Shortcuts"
   - Or find it in Applications folder

2. **Create a New Shortcut**
   - Click the **"+"** button in the top toolbar (or top-right corner)
   - This creates a new blank shortcut

3. **Add the Shell Script Action**
   - In the search bar on the right side, type: **"Run Shell Script"**
   - Click or drag **"Run Shell Script"** into your workflow area

4. **Configure the Script**
   - In the script box that appears, DELETE any existing text
   - Type or paste this EXACT path:
     ```
     ~/.local/bin/scrub
     ```
   - Make sure there are NO extra spaces or quotes

5. **Name Your Shortcut**
   - At the top of the screen, you'll see "New Shortcut" or similar
   - Click on it and rename to: **"Scrub Clipboard"**

6. **Add Keyboard Shortcut** (This is the tricky part!)
   
   **IMPORTANT:** The keyboard shortcut option is NOT in Shortcuts.app itself!
   
   You need to:
   - **Save/Close** the shortcut first (it auto-saves)
   - Go to **System Settings** (or System Preferences on older macOS)
   - Go to **Keyboard**
   - Click **Keyboard Shortcuts** (left sidebar)
   - Click **Services** in the left list
   - Scroll down in the right panel to find **"Scrub Clipboard"** under "General"
   - Click on "Scrub Clipboard" - a button should appear on the right
   - Click **"Add Shortcut"** button
   - Press your desired key combo (e.g., `Cmd+Shift+V`)

---

## Method 2: Using Automator (Works on ALL macOS versions)

This method is more reliable and works on older macOS versions:

### Step-by-Step Instructions:

1. **Open Automator**
   - Press `Cmd+Space` and type "Automator"
   - Or find it in Applications folder

2. **Create a Quick Action**
   - Click **"New Document"** (or File → New)
   - Choose **"Quick Action"** (or "Service" on older macOS)
   - Click **Choose**

3. **Configure the Workflow**
   - At the top, set:
     - **"Workflow receives:"** → select **"no input"**
     - **"in"** → select **"any application"**

4. **Add Shell Script Action**
   - In the search box (left side), type: **"Run Shell Script"**
   - Double-click **"Run Shell Script"** or drag it to the right panel

5. **Configure the Script**
   - In the script text box, DELETE any existing text
   - Type or paste:
     ```
     ~/.local/bin/scrub
     ```
   - Make sure **Shell:** is set to **/bin/bash** or **/bin/zsh**

6. **Save the Quick Action**
   - Press `Cmd+S` or File → Save
   - Name it: **"Scrub Clipboard"**
   - Click **Save**

7. **Assign Keyboard Shortcut**
   - Open **System Settings** (or System Preferences)
   - Go to **Keyboard**
   - Click **Keyboard Shortcuts** (or just "Shortcuts")
   - Click **Services** in the left sidebar
   - Scroll down to find **"Scrub Clipboard"** under "General"
   - Check the checkbox next to it to enable it
   - Click on the right side of "Scrub Clipboard" to add shortcut
   - Press your desired keys (e.g., `Cmd+Shift+V` or `Ctrl+Shift+S`)

---

## Method 3: Simple Alfred/Raycast Alternative

If you use **Alfred** or **Raycast**:

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

Choose one that doesn't conflict:

- `Cmd+Shift+V` - Similar to "paste without formatting"
- `Ctrl+Shift+S` - Easy to remember (S for Scrub)
- `Cmd+Option+V` - Alternative paste shortcut
- `Ctrl+Option+C` - After copying

**Test if shortcut is taken:** Try pressing it in any app first!

---

## Testing Your Shortcut

1. Copy some text with PII:
   ```
   echo "My name is John Smith, email: john@test.com" | pbcopy
   ```

2. Press your keyboard shortcut

3. Paste somewhere (Cmd+V):
   ```
   Should see: My name is <PERSON>, email: <EMAIL_ADDRESS>
   ```

---

## Troubleshooting

### "Shortcut didn't work"
- Make sure you enabled it in System Settings → Keyboard → Shortcuts → Services
- Check the checkbox next to "Scrub Clipboard"
- Try the shortcut again

### "Can't find Scrub Clipboard in Services"
- Close and reopen System Settings
- Log out and log back in
- Restart your Mac

### "Permission denied" errors
- System Settings → Privacy & Security → Automation
- Allow Shortcuts or Automator to control Terminal/System Events

### "Still not working"
- Test manually first: Open Terminal and run `scrub --version`
- Make sure the path is EXACTLY: `~/.local/bin/scrub`
- No quotes, no extra spaces

---

## Quick Manual Test

Before setting up the shortcut, test it works:

```bash
# Copy something
echo "Test: Bob Jones, SSN 123-45-6789" | pbcopy

# Run scrub manually
~/.local/bin/scrub

# Paste to check
pbpaste
# Should show: Test: <PERSON>, <ORGANIZATION> 123-45-6789
```

If this works, the shortcut will work too!

---

## Need Help?

If you're still stuck, tell me:
1. Which macOS version you're on (run: `sw_vers`)
2. Which method you tried (Shortcuts.app or Automator)
3. What happened when you pressed the keyboard shortcut

I can help debug further!
