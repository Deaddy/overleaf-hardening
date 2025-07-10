#!/usr/bin/python3

import sys
import os
import shutil
import tempfile
import subprocess

debug = False

if debug:
    with open("/tmp/latexmkwrapper.log", "w") as f:
        f.write("Command: " + " ".join(sys.argv))

pwd = os.getcwd()

# Ensure auxdir and outdir are the current working directory
# If this changes in the future, this wrapper has to be adapted
assert f"-auxdir={pwd}" in sys.argv
assert f"-outdir={pwd}" in sys.argv


with tempfile.TemporaryDirectory() as tmpdirname:
    shutil.copytree(pwd, tmpdirname, dirs_exist_ok=True)

    custom_args = []

    for arg in sys.argv:
        custom_args.append(arg.replace(pwd, tmpdirname))
    custom_args[0] = "latexmkoriginal"
    print(custom_args)
    subprocess.call(custom_args, cwd=tmpdirname)

    shutil.copytree(tmpdirname, pwd, dirs_exist_ok=True)
