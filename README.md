# Kurumi Says "My Honey"

Bring Tokisaki Kurumi's "My Honey" energy straight into Anki. Ten seconds after
Anki launches, Kurumi lovingly appears with a short audio clip, then repeats the
visit every 30 minutes for five seconds. Both the visual overlay and the audio
use the included media files.

## How it works

- After a 10 second delay, the add-on shows the `my honey screenshot.png` image
  in a frameless overlay sized to the main Anki window.
- Simultaneously, it plays the bundled `my-honey-by Kurumi.mp3` audio file.
- The overlay automatically disappears five seconds later.
- The reminder repeats on a 30 minute interval for as long as Anki stays open.

The Python entry point is stored in the `kurumi says my honey.py` module and is
loaded from `__init__.py` so the add-on remains compatible with Anki's
packaging expectations.

## Media credits

- **Image**: `my honey screenshot.png`
- **Audio**: `my-honey-by Kurumi.mp3`

Please ensure you have the rights to redistribute these assets if you publish
the add-on.

## Testing

From the repository root you can at least check that the Python files compile:

```bash
python -m compileall .
```

Launch Anki with the add-on installed to manually verify the timed overlay and
audio playback.

## Creating and publishing an Anki add-on

1. **Prepare your add-on folder**
   - Include an `__init__.py` file; Anki loads this on startup.
   - Add any supporting Python modules, media files, and a `manifest.json` if
     you need to specify metadata for the add-on manager.
   - Test the add-on locally inside your Anki add-ons directory.
2. **Package the add-on**
   - Zip the add-on folder contents (not the folder itself) so that `__init__.py`
     lives at the archive root.
   - Confirm the archive structure by extracting it into a temporary directory
     and checking the layout.
3. **Create an AnkiWeb listing**
   - Log in to [AnkiWeb](https://ankiweb.net/) and open the *Add-ons* section.
   - Click **Upload Add-on** and provide a name, description, screenshots, and
     version notes. Mention any dependencies or platform-specific details.
   - Upload the ZIP archive you prepared earlier.
4. **Share the code** (optional but recommended)
   - Publish the source on a platform like GitHub so users can review and
     contribute improvements.
   - Add installation instructions and changelog entries to your README.
5. **Maintain the release**
   - Respond to user feedback, fix bugs, and bump the version when you update
     the add-on.

For more details, consult the [official Anki add-on guide](https://addon-docs.ankiweb.net/).

