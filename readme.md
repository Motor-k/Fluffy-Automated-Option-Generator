# Fluffy Automated Option Generator

A simple Tkinter-based tool to inject customized `modinfo.ini` and `screenshot.png` into each top-level folder within a ZIP archive, based on an original metadata INI and image.

Meant to be used together with [Nexus Information Fetcher](https://github.com/Motor-k/Nexusmods-Info-Fetcher) a program that allows the user to specify a game name and a mod id and automatically get its information from [nexusmods](https://www.nexusmods.com/) for use in conjunction with [fluffy mod manager](https://www.nexusmods.com/site/mods/818)
---

## Libraries Used

- **tkinter** (standard library)

  - Provides the graphical user interface for selecting files and running the injection process.

- **requests** (third-party)

  - Used to fetch and download files if extending the tool; not directly used in this GUI-only script but required for the companion fetcher.
  - Installed via `pip install requests`.

- **configparser** (standard library)

  - Reads the original `modinfo.ini` metadata and writes new INI files for each folder.

- **zipfile** (standard library)

  - Reads from and writes to ZIP archives.

- **tempfile**, **shutil**, **os**, **io** (standard library)

  - Handle temporary file creation, atomic replacement of the ZIP archive, file I/O operations, and in-memory string buffers.

---

## Requirements

- Python **3.6** or newer
- **requests** library (for companion app [Nexus Information Fetcher](https://github.com/Motor-k/Nexusmods-Info-Fetcher))

Install third-party dependencies with:

```bash
pip install -r requirements.txt
```
or `install requirements.bat`

> **Note:** `tkinter`, `configparser`, `zipfile`, `tempfile`, `shutil`, `os`, and `io` are part of the Python standard library and require no additional installation.

---

## Files

- `run_GUI.bat`\
  A simple configurable batch file to run the GUI version of the program.

- `Fluffy_Automated_Option_Generator_GUI.py`\
  Main GUI script to select your ZIP archive, original `modinfo.ini`, and `screenshot.png`, then inject new files into each folder.

- `NoGui\Fluffy_Automated_Option_Generator.py`\
  Main script to select your ZIP archive, original `modinfo.ini`, and `screenshot.png`, then inject new files into each folder.

- `NoGui\run.bat`\
  A simple configurable batch file to run the no GUI version of the program with pre-set variables.

- `requirements.txt`\
  Specifies `requests>=2.25.1`.

---

## How to Run

1. Ensure `Fluffy_Automated_Option_Generator_GUI.py` and `requirements.txt` are in the same directory.
2. (Optional) Run `install requirements.bat`
3. Run `run_GUI.bat`
4. In the window that appears:
   - **ZIP File:** Browse to the target ZIP archive containing mod folders.
   - **Original INI:** Browse to the source `modinfo.ini` (with metadata fields).
   - **Screenshot PNG:** Browse to the source `screenshot.png` image file.
   - Click **Run**.

On success, the selected ZIP will be updated in place, with each top-level folder containing:

- A new `modinfo.ini` where:

  ```ini
  [ModInfo]
  name        = <folder name>
  version     = <original version>
  description = <original description>
  author      = <original author>
  category    = costumes
  homepage    = <original homepage>
  nameasbundle= <original mod name>
  ```

- A copy of `screenshot.png`.

---

## Troubleshooting

- **Missing files**: Ensure all three inputs are valid paths.
- **Permissions**: Make sure you have write access to the ZIP file.
- **Python errors**: Confirm you're using Python 3.6+ and that `requests` is installed.

Developed by : Gustavo Bule