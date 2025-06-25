#!/usr/bin/env python3
import argparse
import configparser
import io
import os
import shutil
import tempfile
import zipfile

def read_original_ini(path):
    cp = configparser.ConfigParser()
    cp.read(path)
    s = cp["ModInfo"]
    return {
        "name":        s.get("name", ""),
        "version":     s.get("version", ""),
        "description": s.get("description", ""),
        "author":      s.get("author", ""),
        "homepage":    s.get("homepage", "")
    }

def process_zip(zip_path, ini_path, screenshot_path):
    # 1) Read the original modinfo.ini
    orig = read_original_ini(ini_path)
    original_name = orig["name"]
    version       = orig["version"]
    description   = orig["description"]
    author        = orig["author"]
    homepage      = orig["homepage"]
    category      = "costumes"

    # 2) Load screenshot into memory
    with open(screenshot_path, "rb") as f:
        snapshot_bytes = f.read()

    # 3) Prepare a temp ZIP to write into
    tmp_fd, tmp_zip_path = tempfile.mkstemp(suffix=".zip")
    os.close(tmp_fd)

    with zipfile.ZipFile(zip_path, "r") as zin, \
         zipfile.ZipFile(tmp_zip_path, "w") as zout:

        # Copy all existing entries verbatim
        for info in zin.infolist():
            data = zin.read(info.filename)
            zout.writestr(info, data)

        # Discover all top-level folders
        all_names = zin.namelist()
        top_dirs = {name.split("/",1)[0] for name in all_names if "/" in name}

        for d in top_dirs:
            # Build the new modinfo.ini for this folder
            cp = configparser.ConfigParser()
            cp["ModInfo"] = {
                "name":         d,
                "version":      version,
                "description":  description,
                "author":       author,
                "category":     category,
                "homepage":     homepage,
                "nameasbundle": original_name
            }
            buf = io.StringIO()
            cp.write(buf)
            ini_contents = buf.getvalue()

            # Inject modinfo.ini and screenshot.png into that folder
            zout.writestr(f"{d}/modinfo.ini", ini_contents)
            zout.writestr(f"{d}/screenshot.png", snapshot_bytes)

    # 4) Replace the original zip
    shutil.move(tmp_zip_path, zip_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Inject customized modinfo.ini + screenshot.png into every folder in a ZIP"
    )
    p.add_argument("zipfile",      help="Path to the ZIP archive to update")
    p.add_argument("--ini",        default="modinfo.ini",
                   help="Original modinfo.ini (contains the mod’s metadata)")
    p.add_argument("--screenshot", default="screenshot.png",
                   help="Original screenshot.png to repurpose")
    args = p.parse_args()

    process_zip(args.zipfile, args.ini, args.screenshot)
    print(f"Updated {args.zipfile} successfully.")
