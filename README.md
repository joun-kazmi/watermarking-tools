# Watermarking Tools

Two small desktop GUI tools for watermarking images, written in Python 2.7. They tackle the
same general problem — proving an image's provenance/timestamp — with two different
techniques: an **invisible**, cryptographically-verifiable watermark, and a **visible**,
human-readable timestamp stamp.

## invisible/ — Invisible (steganographic) watermarking

A Tkinter app that embeds a hidden, verifiable timestamp into an image using a simple
visual-cryptography / XOR scheme, then lets you verify it later.

How it works, based on the actual pipeline in `app.py`:

1. **Key** (`key.py`) — generates a random 152x10 black-and-white bitmap used as a shared
   secret.
2. **Timestamp** (`watermarking.py`) — renders the current date/time as a small bitmap,
   using digit glyphs sliced out of `number.png`.
3. **Share** (`key.py`) — XORs the timestamp bitmap with the key bitmap to produce a
   "share" image (a (2,2) visual secret-sharing scheme).
4. **Watermark** (`watermarking.py`) — embeds the share into the target image by flipping
   the least-significant bit of the blue channel of each pixel, and saves the result as
   `watermarked.png`. The change is imperceptible to the eye.
5. **Verify** (`auth.py`) — extracts the LSBs from a watermarked image, XORs them back
   against the original key, and reconstructs the hidden timestamp bitmap so you can
   confirm the watermark is present and matches the key that made it.

Run it with:

```
cd invisible
python app.py
```

Buttons in the GUI walk through the steps in order (`key` -> `timestamp` -> `share` ->
pick an `image` -> `watermark` -> `verify`). `setup.py` is the original `py2exe` build
script used to package the app as a standalone Windows `.exe`; it's kept for reference but
isn't needed to run the app from source. `kaist.gif` and `lena.jpg` are sample images used
for manual testing.

## visible/ — Visible watermarking (date stamping)

A separate Tkinter app (`vis.py`) that batch-processes a folder of JPEGs and stamps each
one with a visible, semi-transparent timestamp in the lower-right corner (the file's EXIF
date if available, otherwise its modification time). Unlike the invisible tool, this
watermark is meant to be seen, not hidden or cryptographically verified — it's a simple
photo-dating utility.

Run it with:

```
cd visible
python vis.py
```

Pick a directory in the GUI; every `.jpg`/`.jpeg` file gets a `-dated` copy saved alongside
the original. `setup.py` here is likewise the original `py2exe` packaging script.

## What they're built with

- **Python 2.7** (both use `print` statements, old-style `Tkinter`/`tkFileDialog` imports,
  and integer division assumptions that are Python-2-specific)
- **PIL** (the pre-Pillow-fork `Python Imaging Library`) for all image manipulation
- **Tkinter** for the GUI
- **py2exe**, originally used to package each tool as a Windows executable (the build
  output itself has been removed from this repo — see below)

## Note on history and cleanup

Both tools originally shipped with their compiled `py2exe` output (`dist/`) committed
alongside the source — a `python27.dll`, a bundled Tcl/Tk runtime, `.pyd` extension
modules, and a `library.zip`, roughly 10-15MB of build artifacts per project. Those have
been removed from version control (see `.gitignore`); they added no value in a git history
and, being mostly Tcl scripts, badly skewed this repository's language statistics away from
the actual Python source.

## Honesty note

These are early, small personal projects from 2016, written against Python 2.7 (now
end-of-life) and PIL. They're kept here as-is — unported, unmodified — as a record of
early work, not as actively maintained tools. Don't expect them to run out of the box on a
modern Python 3 environment without porting.
