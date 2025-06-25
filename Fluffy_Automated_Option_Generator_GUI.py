#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
import io
import os
import shutil
import tempfile
import zipfile

# Core logic from inject_modinfo.py

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
    # Read original metadata
    orig = read_original_ini(ini_path)
    original_name = orig["name"]
    version       = orig["version"]
    description   = orig["description"]
    author        = orig["author"]
    homepage      = orig["homepage"]
    category      = "costumes"

    # Read screenshot bytes
    with open(screenshot_path, "rb") as f:
        snapshot_bytes = f.read()

    # Temporary output ZIP
    tmp_fd, tmp_zip = tempfile.mkstemp(suffix=".zip")
    os.close(tmp_fd)

    try:
        with zipfile.ZipFile(zip_path, "r") as zin, zipfile.ZipFile(tmp_zip, "w") as zout:
            # Copy original entries
            for info in zin.infolist():
                data = zin.read(info.filename)
                zout.writestr(info, data)
            # Find top-level dirs
            names = zin.namelist()
            top_dirs = {n.split('/',1)[0] for n in names if '/' in n}
            # Inject files
            for d in top_dirs:
                # Create new ini for this folder
                cp = configparser.ConfigParser()
                cp["ModInfo"] = {
                    "name": d,
                    "version": version,
                    "description": description,
                    "author": author,
                    "category": category,
                    "homepage": homepage,
                    "nameasbundle": original_name
                }
                buf = io.StringIO()
                cp.write(buf)
                ini_data = buf.getvalue()

                zout.writestr(f"{d}/modinfo.ini", ini_data)
                zout.writestr(f"{d}/screenshot.png", snapshot_bytes)
        # Replace original
        shutil.move(tmp_zip, zip_path)
        return True, None
    except Exception as e:
        # Clean up
        if os.path.exists(tmp_zip):
            os.remove(tmp_zip)
        return False, str(e)

# GUI

def select_file(entry_widget, filetypes, title):
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)


def on_run():
    zip_path = entry_zip.get().strip()
    ini_path = entry_ini.get().strip()
    shot_path = entry_screenshot.get().strip()
    if not zip_path or not ini_path or not shot_path:
        messagebox.showwarning("Missing fields", "Please select all three files.")
        return
    status.set("Processing...")
    root.update_idletasks()
    success, err = process_zip(zip_path, ini_path, shot_path)
    if success:
        status.set("Done!")
        messagebox.showinfo("Success", f"Updated ZIP:\n{zip_path}")
    else:
        status.set("Error")
        messagebox.showerror("Error", err)

root = tk.Tk()
root.title("Inject ModInfo into ZIP")
root.iconbitmap("resources/icon.ico")
frm = tk.Frame(root, padx=10, pady=10)
frm.pack(fill=tk.BOTH, expand=True)

# ZIP selection
tk.Label(frm, text="ZIP File:").grid(row=0, column=0, sticky='e')
entry_zip = tk.Entry(frm, width=50)
entry_zip.grid(row=0, column=1, padx=5)
btn_zip = tk.Button(frm, text="Browse...", command=lambda: select_file(entry_zip,
                                      [("ZIP files", "*.zip"), ("All files", "*.*")],
                                      "Select ZIP File"))
btn_zip.grid(row=0, column=2)

# INI selection
tk.Label(frm, text="Original INI:").grid(row=1, column=0, sticky='e')
entry_ini = tk.Entry(frm, width=50)
entry_ini.grid(row=1, column=1, padx=5)
btn_ini = tk.Button(frm, text="Browse...", command=lambda: select_file(entry_ini,
                                      [("INI files", "*.ini"), ("All files", "*.*")],
                                      "Select modinfo.ini"))
btn_ini.grid(row=1, column=2)

# Screenshot selection
tk.Label(frm, text="Screenshot PNG:").grid(row=2, column=0, sticky='e')
entry_screenshot = tk.Entry(frm, width=50)
entry_screenshot.grid(row=2, column=1, padx=5)
btn_shot = tk.Button(frm, text="Browse...", command=lambda: select_file(entry_screenshot,
                                      [("PNG images", "*.png"), ("All files", "*.*")],
                                      "Select screenshot.png"))
btn_shot.grid(row=2, column=2)

# Run button
btn_run = tk.Button(frm, text="Run", width=20, command=on_run)
btn_run.grid(row=3, column=0, columnspan=3, pady=10)

# Status bar
status = tk.StringVar(value="Ready")
status_lbl = tk.Label(root, textvariable=status, anchor='w')
status_lbl.pack(fill=tk.X, padx=10, pady=(0,10))

root.mainloop()
